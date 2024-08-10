from odoo import models, fields

class ModuleFasilitas(models.Model):
    _name = 'fasilitas.kamar'
    _description = 'Fasilitas yang ada di kamar hotel.'

    nama = fields.Char(string='Nama',required = True)
    kode = fields.Char(string='Kode',required = True)