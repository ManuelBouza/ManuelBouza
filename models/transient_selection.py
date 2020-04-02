# -*- coding: utf-8 -*-
from openerp import models, fields, api


class TransientSelection(models.TransientModel):
    _name = 'transient.selection'
    _description = 'Transient Selection'

    name = fields.Char(
        string='Nombre',
    )

    model_id = fields.Integer(
        string='Model_id',
        required=False,
    )

    key_id = fields.Char(
        string='Key_id',
        required=False,
    )
