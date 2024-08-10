from odoo import http
from odoo.http import request
import json

class BookingController(http.Controller):

    @http.route('/kamarhotel', type='http', auth='public', methods=['GET'], csrf=False)
    def get_kamarhotel(self, **kwargs):
        KamarHotel = request.env['booking.hotel'].sudo().search([])
        data = []
        for kamarhotel in KamarHotel:
            fasilitas_names = [f.nama for f in kamarhotel.fasilitas]
            transaksi_ids = [t.order_id for t in kamarhotel.history_transaksi]
            tipe_kamar = kamarhotel.tipekamar
            data.append({
                'id': kamarhotel.id,
                'name': kamarhotel.name,
                'tipekamar': tipe_kamar.tipekamar if tipe_kamar else '',
                'floor': kamarhotel.floor,
                'length': tipe_kamar.length if tipe_kamar else 0,
                'width': tipe_kamar.width if tipe_kamar else 0,
                'area': tipe_kamar.area if tipe_kamar else 0,
                'status': kamarhotel.status,
                'price_per_night': tipe_kamar.price_per_night if tipe_kamar else 0,
                'fasilitas': fasilitas_names,
                'history_transaksi': transaksi_ids
            })
        return request.make_response(json.dumps(data), headers={'Content-Type': 'application/json'})

    @http.route('/kamarhotel', type='http', auth='public', methods=['POST'], csrf=False)
    def post_kamarhotel(self, **kwargs):
        KamarHotel = request.env['booking.hotel']
        name = kwargs.get('name')
        floor = kwargs.get('floor')
        tipekamar = kwargs.get('tipekamar')
        fasilitas = kwargs.get('fasilitas')
        
        if not name or not floor or not tipekamar:
            return request.make_response(json.dumps({'error': 'Fields yang diperlukan ada yang tidak lengkap.'}),headers={'Content-Type': 'application/json'})

        try:
            tipekamar_id = int(tipekamar)
            fasilitas_ids = [int(fid) for fid in fasilitas.split(',')] if fasilitas else []
            new_kamarhotel = KamarHotel.sudo().create({
                'name': name,
                'floor': floor,
                'tipekamar': tipekamar_id,
                'status': 'available',
                'fasilitas': [(6, 0, fasilitas_ids)]
            })
            request.env.cr.commit()  
            return request.make_response(json.dumps({'success': True, 'id': new_kamarhotel.id}),headers={'Content-Type': 'application/json'})
        except Exception as e:
            return request.make_response(json.dumps({'error': 'Terjadi error saat menyimpan data.'}),headers={'Content-Type': 'application/json'})

    @http.route('/kamarhotel/<int:kamarhotel_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_kamarhotel(self, kamarhotel_id, **kwargs):
        KamarHotel = request.env['booking.hotel'].sudo().browse(kamarhotel_id)
        if KamarHotel.exists():
            KamarHotel.unlink()
            request.env.cr.commit()  
            return request.make_response(json.dumps({'status': 'Penghapusan kamar sukses.'}), headers={'Content-Type': 'application/json'})
        return request.make_response(json.dumps({'error': 'Catatan tidak ditemukan.'}), headers={'Content-Type': 'application/json'})