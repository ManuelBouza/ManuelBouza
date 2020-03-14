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

    rule = fields.One2many(
        comodel_name='rule',
        inverse_name='rules_generator_id',
        string='Reglas',
        required=False,
    )

    @api.multi
    def add_rule(self):

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'rule.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_rules_generator_id': self.id,
                'rule_model_id': self.rule_model.id,
                'create': True,
            },
        }