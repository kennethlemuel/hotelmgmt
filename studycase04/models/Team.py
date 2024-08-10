from odoo import models, fields, api

class TeamModel(models.Model):
    _name = "team.model"
    _description = "Deskripsi team Sales"
    _rec_name = "teamname"

    teamname = fields.Char(string="Team Name", default="", required=True)
    salesleader = fields.Many2one('res.users', string="Sales Leader", domain=lambda self: [('groups_id', 'in', [self.env.ref('studycase04.group_supervisor').id])])
    salesperson = fields.Many2many('res.users', string="Sales Person", domain=lambda self: [('groups_id', 'in', [self.env.ref('studycase04.group_user').id])])
    total_transaksi = fields.Float(string="Total Transaksi", compute='_compute_total_transaksi')
    total_komisi = fields.Float(string="Total Komisi", compute='_compute_total_komisi')

    @api.depends('salesleader', 'salesperson')
    def _compute_total_transaksi(self):
        for team in self:
            transactions = self.env['transaksi.model'].search(['|', ('salesperson', 'in', team.salesperson.ids), ('salesperson', '=', team.salesleader.id), ('status', 'in', ['active', 'finish'])])
            team.total_transaksi = sum(transactions.mapped('total_price'))

    @api.depends('total_transaksi')
    def _compute_total_komisi(self):
        komisi = self.env['ir.config_parameter'].sudo().get_param('value.komisi', default=0)
        for team in self:
            team.total_komisi = team.total_transaksi * (float(komisi) / 100)

    def get_transaksi(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window','name': 'Transactions','view_mode': 'tree','res_model': 'transaksi.model','domain': [('status', '=', 'active'), ('salesteam', '=', self.id)],'context': "{'create': False}"}


