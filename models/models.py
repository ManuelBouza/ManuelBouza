# -*- coding: utf-8 -*-

from openerp import models, fields, api

# class audit_v3(models.Model):
#     _name = 'audit_v3.audit_v3'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100