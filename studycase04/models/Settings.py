from odoo import models,fields,api

class SettingsModel(models.TransientModel):
    _inherit = "res.config.settings"

    komisi = fields.Integer(string="Komisi", readonly = False, config_parameter = 'komisi')

    def set_values(self):
        res = super(SettingsModel, self).set_values()
        self.env['ir.config_parameter'].set_param('value.komisi',self.komisi)
        return res
    
    @api.model
    def get_values(self):
        res = super(SettingsModel, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        values = ICPSudo.get_param('value.komisi')
        res.update(komisi=values)
        return res
    


