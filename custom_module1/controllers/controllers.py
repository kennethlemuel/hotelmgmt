# -*- coding: utf-8 -*-
# from odoo import http


# class CustomModule1(http.Controller):
#     @http.route('/custom_module1/custom_module1', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_module1/custom_module1/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_module1.listing', {
#             'root': '/custom_module1/custom_module1',
#             'objects': http.request.env['custom_module1.custom_module1'].search([]),
#         })

#     @http.route('/custom_module1/custom_module1/objects/<model("custom_module1.custom_module1"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_module1.object', {
#             'object': obj
#         })
