# -*- coding: utf-8 -*-
from openerp import models, fields, api


class RulesGenerator(models.Model):
    _name = 'rules.generator'
    _description = 'Rules Generator'

    name = fields.Char(
        string='Nombre',
        required=True,
    )

    description = fields.Text(
        string="Descripción",
        required=False,
    )

    rule_model = fields.Many2one(
        comodel_name='ir.model',
        string='Rule_model',
        required=True
    )

    fields_show_result = fields.Many2many(
        comodel_name='ir.model.fields',
        string='Campos a Mostrar en Resultado',
    )

    rules = fields.One2many(
        comodel_name='rule',
        inverse_name='rule_generator_id',
        string='Reglas',
        required=False,
    )
