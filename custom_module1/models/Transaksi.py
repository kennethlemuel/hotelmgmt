from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ModelTransaksi(models.Model):
    _name = 'transaksi.model'
    _description = 'Transaksi-transaksi kustomer'
    _rec_name = 'member'

    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Aktif'),
        ('finish', 'Selesai'),
        ('cancel', 'Cancel')
    ], string='Status', default='draft')
    member = fields.Many2one('res.partner', string='Nama Member', required=True)
    kamar = fields.Many2one('booking.hotel', string='Kamar')
    startdate = fields.Date(string='Start Date', required=True)
    enddate = fields.Date(string='End Date', required=True)
    durasi = fields.Integer(string='Durasi (Hari)', compute='_compute_durasi', store=True)
    note = fields.Text(string='Note')

    @api.depends('startdate', 'enddate')
    def _compute_durasi(self):
        for record in self:
            if record.startdate and record.enddate:
                start_date = fields.Date.from_string(record.startdate)
                end_date = fields.Date.from_string(record.enddate)
                record.durasi = (end_date - start_date).days
            else:
                record.durasi = 0

    @api.model
    def create(self, vals):
        record = super(ModelTransaksi, self).create(vals)
        return record

    def write(self, vals):
        record = super(ModelTransaksi, self).write(vals)
        
        return record

    def unlink(self):
        record = super(ModelTransaksi, self).unlink()
        return record

    def _update_kamar_status(self):
        for record in self:
            booked = record.kamar
            if booked:
                if record.status == 'cancel':
                    booked.status = 'available'
                else:
                    available = self.env['booking.hotel'].search([
                        ('name', '=', booked.name),
                        ('status', '=', 'available')
                    ])
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
                    raise ValidationError(_('Kamar sudah dibook pada hari terpilih: %s s.d. %s') % (record.startdate,record.enddate))

    