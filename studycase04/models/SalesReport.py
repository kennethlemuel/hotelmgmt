from odoo import models, fields, api, tools

class SalesReport(models.Model):
    _name = 'sales.report'
    _description = 'Sales Analysis Report'
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    date = fields.Date('Order Date', readonly=True)
    total_price = fields.Float('Total Price', readonly=True)
    salesperson_id = fields.Many2one('res.users', 'Salesperson', readonly=True)
    salesteam_id = fields.Many2one('team.model', 'Sales Team', readonly=True)

    def _select(self):
        return """
            SELECT
                MIN(t.id) AS id,
                t.startdate AS date,
                SUM(t.total_price) AS total_price,
                t.salesperson AS salesperson_id,
                t.salesteam AS salesteam_id
        """

    def _from(self):
        return """
            FROM transaksi_model t
        """

    def _group_by(self):
        return """
            GROUP BY
                t.startdate,
                t.salesperson,
                t.salesteam
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, 'sales_report')
        self._cr.execute("""
            CREATE VIEW sales_report AS (
                %s
                %s
                %s
            )
        """ % (self._select(), self._from(), self._group_by()))
