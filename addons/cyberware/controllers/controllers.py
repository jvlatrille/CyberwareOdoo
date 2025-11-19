# -*- coding: utf-8 -*-
# from odoo import http


# class Cyberware(http.Controller):
#     @http.route('/cyberware/cyberware', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cyberware/cyberware/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cyberware.listing', {
#             'root': '/cyberware/cyberware',
#             'objects': http.request.env['cyberware.cyberware'].search([]),
#         })

#     @http.route('/cyberware/cyberware/objects/<model("cyberware.cyberware"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cyberware.object', {
#             'object': obj
#         })

