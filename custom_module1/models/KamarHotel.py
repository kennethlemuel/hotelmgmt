# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ModelBooking(models.Model):
    _name = 'booking.hotel'
    _description = 'Detail Booking Hotel'

    name = fields.Char(string='Nama Kamar', required=True)
    tipekamar = fields.Many2one('tipe.kamar', string='Tipe Kamar')
    floor = fields.Integer(string='Lantai', required=True)
    status = fields.Selection([('available', 'Available'),('booked', 'Booked')], string='Status', default='available', readonly = True)
    fasilitas = fields.Many2many('fasilitas.kamar', string='Fasilitas')
    history_transaksi = fields.One2many('transaksi.model', 'member', string='History Booking')



    