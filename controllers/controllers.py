# -*- coding: utf-8 -*-
from openerp import http

# class AuditV3(http.Controller):
#     @http.route('/audit_v3/audit_v3/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/audit_v3/audit_v3/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('audit_v3.listing', {
#             'root': '/audit_v3/audit_v3',
#             'objects': http.request.env['audit_v3.audit_v3'].search([]),
#         })

#     @http.route('/audit_v3/audit_v3/objects/<model("audit_v3.audit_v3"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('audit_v3.object', {
#             'object': obj
#         })