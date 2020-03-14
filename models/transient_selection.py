# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Many2mayValue(models.Model):
    _name = 'many2many.value'
    _description = 'Many2many Value'

    name = fields.Char(
        string='Nombre',
    )

    model_id = fields.Integer(
        string='Model_id',
        required=False,
    )

class Many2oneValue(models.Model):
    _name = 'many2one.value'
    _description = 'Many2one Value'

    name = fields.Char(
        string='Nombre',
    )

    model_id = fields.Integer(
        string='Model_id',
        required=False,
    )

class SelectionValue(models.Model):
    _name = 'selection.value'
    _description = 'Many2one Value'

    key_id = fields.Char(
        string='Nombre',
    )

    name = fields.Char(
        string='Nombre',
    )

