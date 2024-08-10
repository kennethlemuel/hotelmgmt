from odoo import models, fields, api

class ModuleMember(models.Model):
    _inherit = 'res.partner'

    history = fields.One2many('transaksi.model', 'member', string="History", domain=[('status', '=', 'active')])
    booking_count = fields.Integer(string='Booking Aktif', compute='compute_active', store=True)

    @api.depends('history.status')
    def compute_active(self):
        for record in self:
            active_bookings = record.history.filtered(lambda r: r.status == 'active')
            record.booking_count = len(active_bookings)

    def get_booking(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window','name': 'Booking','view_mode': 'tree','res_model': 'transaksi.model','domain': [('status', '=', 'active'), ('member', '=', self.id)],'context': "{'create': False}"}
