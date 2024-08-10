from odoo import models, fields, api

class ModuleMember(models.Model):
    _inherit = 'res.partner'

    history = fields.One2many('transaksi.model', 'member', string="History", domain=[('status', '=', 'active')])
    
