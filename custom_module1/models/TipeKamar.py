from odoo import models, fields, api

class ModelTipeKamar(models.Model):
    _name = 'tipe.kamar'
    _description = 'Tipe dan Harga Kamar'
    _rec_name = "tipekamar"
    
    tipekamar = fields.Char(string='Tipe Kamar', required = True)
    length = fields.Float(string='Panjang (m)', required=True)
    width = fields.Float(string='Lebar (m)', required=True)
    area = fields.Float(string='Luas (sq m)', compute='_compute_area', store=True)
    price_per_night = fields.Float(string='Harga per malam (Rp.)', required=True) 

    @api.depends('length', 'width')
    def _compute_area(self):
        for kamar in self:
            kamar.area = kamar.length * kamar.width  

   