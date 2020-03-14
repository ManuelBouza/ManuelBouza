# -*- coding: utf-8 -*-
from openerp import models, fields, api


class ruleWizard(models.TransientModel):
    _name = 'rule.wizard'
    _description = 'rule Wizard'
    _inherit = 'rule'

    date_value = fields.Date(
        string='Date',
        required=False,
    )

    date_time_value = fields.Datetime(
        string='Date_time_value',
        required=False,
    )

    integer_value = fields.Integer(
        string='integer_value',
        required=False,
    )

    bool_value = fields.Boolean(
        string='Bool_value',
        required=False,
    )

    char_value = fields.Char(
        string='Char_value',
        required=False,
    )

    float_value = fields.Float(
        string='Float_value',
        required=False,
    )

    many2many_value = fields.Many2many(
        comodel_name='many2many.value',
        string='Many2many_value',
    )

    many2one_value = fields.Many2one(
        comodel_name='many2one.value',
        string='Many2many_value',
    )

    selection_value = fields.Many2one(
        comodel_name='selection.value',
        string='Many2many_value',
    )
