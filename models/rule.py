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

    many2many_values = fields.Many2many(
        comodel_name='many2many.values',
        string='Relational_value',
    )

    many2one_values = fields.Many2one(
        comodel_name='many2one.values',
        string='Many2One_values',
    )

    selection_values = fields.Many2one(
        comodel_name='selection.values',
        string='Selection_values',
    )

    @api.depends('rule_field')
    def _compute_fields_type(self):
        if self.rule_field:
            self.fields_type = self.rule_field.ttype



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

            ######################## Debug ##########################################################
            import sys
            sys.path.append("/usr/lib/python2.7/debug/pydevd-pycharm.egg")
            import pydevd_pycharm
            pydevd_pycharm.settrace('10.0.75.1', port=4020, stdoutToServer=True, stderrToServer=True)
            ######################## Debug ##########################################################

            ids_to_rel = self.many2one_values.ids
            context['default_many2one_values'] = [(6, 0, ids_to_rel)]


        # elif self.fields_type in ['many2many', 'many2one', 'selection']:
        #     context['default_selection_values'] = self.selection_values.id

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'rule.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }


