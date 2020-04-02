# -*- coding: utf-8 -*-
from openerp import models, fields, api


class RelationalValues(models.Model):
    _name = 'relational.values'
    _description = 'Relational Values'

    name = fields.Char(
        string='Nombre',
    )

    model_id = fields.Integer(
        string='Model_id',
        required=False,
    )


class SelectionValues(models.Model):
    _name = 'selection.values'
    _description = 'Selection Values'

    key_id = fields.Char(
        string='Nombre',
    )

    name = fields.Char(
        string='Nombre',
    )
