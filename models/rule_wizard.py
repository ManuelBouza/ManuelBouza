# -*- coding: utf-8 -*-
from openerp import models, fields, api


class ruleWizard(models.TransientModel):
    _name = 'rule.wizard'
    _description = 'rule Wizard'
    _inherit = 'rule'

    @api.onchange('rule_field')
    def onchange_method(self):

        if not self.env.context.get('edit', False):

            if self.fields_type in ['many2many']:

                ######################## Debug ##########################################################
                import sys
                sys.path.append("/usr/lib/python2.7/debug/pydevd-pycharm.egg")
                import pydevd_pycharm
                pydevd_pycharm.settrace('10.0.75.1', port=4020, stdoutToServer=True, stderrToServer=True)
                ######################## Debug ##########################################################

                transient_ids = []
                rule_model = self.rule_field.relation  # esto es el modelo
                records = self.env[rule_model].search([])
                rule_id = self.env.context.get('rule_model_id')


                for record in records:
                    transient = self.env['many2many.values'].create(
                        {
                            'name': record.name,
                            'model_id': record.id,
                        }
                    )
                    transient_ids.append(transient.id)

                return {'domain': {'many2many_values': [('id', 'in', transient_ids)]}}

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

                    # if not self.selection_values:
                    #     self.selection_values = [(6, 0, transient_ids)]

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
            rule['datetime'] = self.date_time_value
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

            ######################## Debug ############################################################
            import sys
            sys.path.append("/usr/lib/python2.7/debug/pydevd-pycharm.egg")
            import pydevd_pycharm
            pydevd_pycharm.settrace('10.0.75.1', port=4020, stdoutToServer=True, stderrToServer=True, )
            ######################## Debug ############################################################

            ids_to_rel = self.many2many_values.ids
            rule['many2many_values'] = [(6, 0, ids_to_rel)]

            many2one_values = self.env['many2many.values'].search([('rule_id', '=', self.id)]).ids

            name = []

            for value in self.many2many_values:
                name.append(value.name)

            rule['shown_value'] = "".join(name)


        elif fields_type in ['selection', 'many2one']:

            ######################## Debug ############################################################
            import sys
            sys.path.append("/usr/lib/python2.7/debug/pydevd-pycharm.egg")
            import pydevd_pycharm
            pydevd_pycharm.settrace('10.0.75.1', port=4020, stdoutToServer=True, stderrToServer=True, )
            ######################## Debug ############################################################

            rule['selection_values'] = self.selection_values.id
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
