# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Rule(models.Model):
    _name = 'rule'
    _description = 'Rule'
    _order = 'sequence'

    sequence = fields.Integer(
        string='Secuencia',
        default=0,
        required=True,
    )

    # el name deja de usarse ahora!!!....
    name = fields.Char(
        string='Name',
        required=False,
    )

    rules_generator_id = fields.Many2one(
        comodel_name='rules.generator',
        string='Rules Generator',
        required=True,
        ondelete='cascade',
    )

    fields_type = fields.Char(
        compute='_compute_fields_type',
        store=True,
    )

    ####################
    # Tree value Shown #
    ####################
    rule_field = fields.Many2one(
        comodel_name='ir.model.fields',
        string='Rule_field',
        required=True,
    )

    logical_operator = fields.Many2one(
        comodel_name='logical.operators',
        string='logical_operator',
        required=True,
    )

    shown_value = fields.Char(
        string=' shown_value',
        required=False,
    )

    ##############
    # Data Types #
    ##############
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

    ###########################
    # Data Types Relational id#
    ###########################
    many2many_selected_id = fields.Integer(
        string='Relational_value',
        required=False,
    )

    many2one_selected_id = fields.Integer(
        string='Many2One_values',
        required=False,
    )

    selection_selected_id = fields.Integer(
        string='Selection_values',
        required=False,
    )

    @api.multi
    def edit(self):


        context = {
            'default_rules_generator_id': self.rules_generator_id.id,
            'default_rule_model': self.rules_generator_id.rule_model.id,
            'default_rule_field': self.rule_field.id,
            'default_logical_operator': self.logical_operator.id,
            'edit': True,
            'rule_id': self.id,
        }

        domain = {}

        if self.fields_type == 'date':
            context['default_date_value'] = self.date_value

        elif self.fields_type == 'datetime':


            context['default_date_time_value'] = self.date_time_value

        elif self.fields_type == 'integer':
            context['default_integer_value'] = self.integer_value

        elif self.fields_type == 'boolean':
            context['default_bool_value'] = self.bool_value

        elif self.fields_type == 'char':
            context['default_char_value'] = self.char_value

        elif self.fields_type in ['float', 'monetary']:
            context['default_float_value'] = self.float_value

        elif self.fields_type in ['many2many']:
            context['default_many2many_selected_id'] = self.many2many_selected_id

        elif self.fields_type in ['many2one']:
            context['default_many2one_selected_id'] = self.many2one_selected_id

        elif self.fields_type in ['selection']:
            context['default_selection_selected_id'] = self.selection_selected_id

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'rule.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }
