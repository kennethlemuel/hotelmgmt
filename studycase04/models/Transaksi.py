from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class ModelTransaksi(models.Model):
    _name = 'transaksi.model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Transaksi-transaksi kustomer'
    _rec_name = 'member'

    order_id = fields.Char(string='Order ID', readonly=True)
    status = fields.Selection([('draft', 'Draft'), ('active', 'Aktif'), ('finish', 'Selesai'), ('cancel', 'Cancel')], string='Status', default='draft')
    member = fields.Many2one('res.partner', string='Nama Member', required=True)
    salesperson = fields.Many2one('res.users', string='Sales Person', required=False, default=lambda self: self.env.user, readonly=True)
    salesteam = fields.Many2one('team.model', string='Sales Team', compute='_compute_salesteam', store=True, readonly=True)
    kamar = fields.Many2one('booking.hotel', string='Kamar', required=True, ondelete = "cascade")
    startdate = fields.Date(string='Start Date', required=True)
    enddate = fields.Date(string='End Date', required=True)
    durasi = fields.Integer(string='Durasi (Hari)', compute='_compute_durasi', store=True)
    total_price = fields.Float(string='Total Harga (Rp.)', compute='_compute_total_price', store=True)
    note = fields.Text(string='Note')

    @api.depends('salesperson')
    def _compute_salesteam(self):
        for record in self:
            if record.salesperson:
                team = self.env['team.model'].search([('salesleader', '=', record.salesperson.id)], limit=1)
                if not team:
                    team = self.env['team.model'].search([('salesperson', 'in', [record.salesperson.id])], limit=1)
                record.salesteam = team

    @api.depends('startdate', 'enddate')
    def _compute_durasi(self):
        for record in self:
            if record.startdate and record.enddate:
                start_date = fields.Date.from_string(record.startdate)
                end_date = fields.Date.from_string(record.enddate)
                record.durasi = (end_date - start_date).days
            else:
                record.durasi = 0

    @api.depends('durasi', 'kamar')
    def _compute_total_price(self):
        for record in self:
            if record.durasi and record.kamar:
                room_type = self.env['tipe.kamar'].search([('id', '=', record.kamar.tipekamar.id)], limit=1)
                if room_type:
                    record.total_price = record.durasi * room_type.price_per_night
                else:
                    record.total_price = 0
            else:
                record.total_price = 0

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('transaksi.model.order') or '/'
        start_date_str = datetime.strptime(vals['startdate'], '%Y-%m-%d').strftime('%Y/%m')
        vals['order_id'] = f"ORD/{start_date_str}/{seq[-3:]}"
        record = super(ModelTransaksi, self).create(vals)
        return record

    def write(self, vals):
        result = super(ModelTransaksi, self).write(vals)
        return result

    def unlink(self):
        result = super(ModelTransaksi, self).unlink()
        return result

    def _update_kamar_status(self):
        for record in self:
            booked = record.kamar
            if booked:
                if record.status == 'cancel':
                    booked.status = 'available'
                else:
                    available = self.env['booking.hotel'].search([('name', '=', booked.name), ('status', '=', 'available')])
                    if available:
                        booked.status = 'booked'
                    else:
                        booked.status = 'available'

    def transaksi_confirm(self):
        self.write({'status': 'active'})
        self._update_kamar_status()
        self._check_kamar_availability()

    def transaksi_cancel(self):
        self.write({'status': 'cancel'})
        self._update_kamar_status()
        self._check_kamar_availability()

    @api.model
    def _auto_finish_bookings(self):
        today = fields.Date.today()
        bookings = self.search([('enddate', '<', today), ('status', '=', 'active')])
        for booking in bookings:
            booking.status = 'finish'
            booking._send_finish_email()

    @api.constrains('kamar', 'startdate', 'enddate')
    def _check_kamar_availability(self):
        for record in self:
            if record.kamar and record.startdate and record.enddate:
                overlapping_bookings = self.search([
                    ('kamar', '=', record.kamar.id),
                    ('id', '!=', record.id),
                    ('status', '!=', 'cancel'),
                    ('startdate', '<=', record.enddate),
                    ('enddate', '>=', record.startdate),
                ])
                if overlapping_bookings:
                    raise ValidationError(_('Kamar sudah dibook pada hari terpilih: %s s.d. %s') % (record.startdate, record.enddate))

    def print_invoice(self):
        if self.status == 'active':
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': self.member.id,
                'invoice_date': fields.Date.today(),
                'invoice_line_ids': [(0, 0, {
                    'product_id': self.kamar.id,
                    'price_unit': self.total_price,
                    'name': f'Booking for room {self.kamar.name} from {self.startdate} to {self.enddate}',  # Description
                })],
                'name': self.order_id
            })

            return self.env.ref('studycase04.custom_invoice_report_action').report_action(invoice)
        else:
            raise ValidationError(_('Tidak bisa kirim invoice untuk transaksi tidak aktif.'))

    def transaksi_confirm(self):
        self.ensure_one()
        self.write({'status': 'active'})
        template_id = self.env.ref('studycase04.email_transaksi_confirmation').id
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)

    def transaksi_finish(self):
        self.ensure_one()
        self.write({'status': 'finish'})
        template_id = self.env.ref('studycase04.email_transaksi_finish').id
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)

    @api.model
    def check_and_send_finished_transactions(self):
        transactions = self.search([('status', '=', 'active')])
        for transaction in transactions:
            if transaction.enddate and transaction.enddate <= fields.Date.today():
                transaction.transaksi_finish()

