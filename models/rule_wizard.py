# -*- coding: utf-8 -*-
from openerp import models, fields, api


class ruleWizard(models.TransientModel):
    _name = 'rule.wizard'
    _description = 'rule Wizard'
    _inherit = 'rule'

    #########################
    # Data Types Relational #
    #########################
    many2many_values = fields.Many2one(
        comodel_name='relational.values',
        string='Relational_value',
    )

    many2one_values = fields.Many2one(
        comodel_name='relational.values',
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

    @api.onchange('rule_field')
    def onchange_method(self):

        #TODO resetear todos los valores si se cambia de opcion.

        if self.fields_type in ['many2many']:

            transient_ids = []

            rule_model = self.rule_field.relation  # esto es el modelo
            records = self.env[rule_model].search([])

            for record in records:
                transient = self.env['relational.values'].create(
                    {
                        'name': record.name,
                        'model_id': record.id,
                    }
                )
                transient_ids.append(transient.id)

                if self.env.context.get('edit', False) and record.id == self.many2many_selected_id:
                    self.many2many_values = transient.id

            return {
                'domain': {'many2many_values': [('id', 'in', transient_ids)]},
                'many2many_values': self.many2many_values,
            }

        elif self.fields_type in ['many2one']:

            transient_ids = []

            rule_model = self.rule_field.relation  # esto es el modelo
            records = self.env[rule_model].search([])

            for record in records:
                transient = self.env['relational.values'].create(
                    {
                        'name': record.name,
                        'model_id': record.id,
                    }
                )
                transient_ids.append(transient.id)

                if self.env.context.get('edit', False) and record.id == self.many2one_selected_id:
                    self.many2one_values = transient.id

            return {
                'domain': {'many2one_values': [('id', 'in', transient_ids)]},
                'many2one_values': self.many2one_values,
            }

        elif self.fields_type == 'selection':

            transient_ids = []

            if not self.rule_field.related:
                selection_value = self.env[
                    self.rules_generator_id.rule_model.model
                ]._fields[self.rule_field.name].selection

                for value in selection_value:
                    key_id = value[0]
                    name = value[1]

                    transient = self.env['selection.values'].create(
                        {
                            'name': name,
                            'key_id': key_id,
                        }
                    )
                    transient_ids.append(transient.id)

                    if self.env.context.get('edit', False) and key_id == self.selection_selected_id:
                        self.selection_values = transient.id

            else:
                related = self.rule_field.related.split('.')
                model_related_name = related[0]
                field_related_name = related[1]

                rule_model_name = self.rules_generator_id.rule_model.model

                model_related = self.env[rule_model_name]._fields[model_related_name]

                selection_values = self.env[
                    model_related.comodel_name
                ]._fields[field_related_name].selection

                for value in selection_values:
                    key_id = value[0]
                    name = value[1]

                    transient = self.env['selection.values'].create(
                        {
                            'name': name,
                            'key_id': key_id,
                        }
                    )
                    transient_ids.append(transient.id)

                    if self.env.context.get('edit', False) and key_id == self.selection_selected_id:
                        self.selection_values = transient.id

            return {'domain': {'selection_values': [('id', 'in', transient_ids)]}}

    @api.multi
    def create_rule(self):
        rule = {
            'generator_id': self.rules_generator_id.id,
            'rule_model': self.rules_generator_id.rule_model.id,
            'rule_field': self.rule_field.id,
            'logical_operator': self.logical_operator.id,
            'fields_type': self.fields_type,
        }

        fields_type = self.fields_type

        if fields_type == 'date':
            rule['date_value'] = self.date_value
            rule['shown_value'] = self.date_value

        elif fields_type == 'datetime':


            rule['date_time_value'] = self.date_time_value
            rule['shown_value'] = self.date_time_value

        elif fields_type == 'integer':
            rule['integer_value'] = str(self.integer_value)
            rule['shown_value'] = str(self.integer_value)

        elif fields_type == 'boolean':
            rule['bool_value'] = self.bool_value
            rule['shown_value'] = "Verdadero" if self.bool_value else "Falso"

        elif fields_type == 'char':
            rule['char_value'] = self.char_value
            rule['shown_value'] = self.char_value

        elif fields_type in ['float', 'monetary']:
            rule['float_value'] = str(self.float_value)
            rule['shown_value'] = str(self.float_value)

        elif fields_type in ['many2many']:

            rule['many2many_selected_id'] = self.many2many_values.model_id
            rule['shown_value'] = self.many2many_values.name

        elif fields_type in ['many2one']:
            rule['many2one_selected_id'] = self.many2one_values.model_id
            rule['shown_value'] = self.many2one_values.name

        elif fields_type in ['selection']:
            rule['selection_values'] = self.selection_values.key_id
            rule['shown_value'] = self.selection_values.name

        else:
            return False
        # programar error

        if self.env.context.get('create', False):
            self.env['rule'].create(rule)

        if self.env.context.get('edit', False):
            self.env['rule'].browse(
                self.env.context.get('rule_id', False)
            ).write(rule)
