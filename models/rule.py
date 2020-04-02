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

    rule_generator_id = fields.Many2one(
        comodel_name='rules.generator',
        string='rules Generator id',
        required=True,
        ondelete='cascade',
    )

    fields_type = fields.Char(
        compute='_compute_fields_type',
        store=True,
    )

    rule_field = fields.Many2one(
        comodel_name='ir.model.fields',
        string='Rule_field',
        required=True,
    )

    logical_operator = fields.Many2one(
        comodel_name='logical.operators',
        string='logical_operator',
        required=True
    )

    selected_value = fields.Char(
        string=' selected_value',
        required=False,
    )

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

    # este campo es para los many2one, many2many y selection
    many2many_value = fields.Many2many(
        comodel_name='transient.selection',
        string='Many2many_value',
    )

    @api.depends('rule_field')
    def _compute_fields_type(self):
        if self.rule_field:
            self.fields_type = self.rule_field.ttype

    @api.onchange('rule_field')
    def onchange_method(self):

        if self.fields_type:
            self.fields_type = self.rule_field.ttype

            if self.fields_type in ['selection', 'many2many', 'many2one']:

                self.many2many_value = False

                transient_ids = []

                if self.fields_type == 'selection':
                    rule_model = self.rule_model.model
                    rule_field = self.rule_field.name

                    if not self.rule_field.related:
                        selection_values = self.env[rule_model]._fields[rule_field].selection
                    else:

                        related = self.rule_field.related.split('.')
                        model_related = related[0]
                        field_related = related[1]

                        model_related = self.env[rule_model]._fields[model_related]
                        selection_values = self.env[model_related.comodel_name]._fields[field_related].selection

                    for value in selection_values:
                        key_id = value[0]
                        name = value[1]

                        transient = self.env['transient.selection'].create(
                            {
                                'name': name,
                                'key_id': key_id,
                            }
                        )

                    transient_ids.append(transient.id)
                else:  # 'many2many', 'many2one'

                    rule_model = self.rule_field.relation  # esto es el modelo
                    records = self.env[rule_model].search([])

                    for record in records:
                        transient = self.env['transient.selection'].create(
                            {
                                'name': record.name,
                                'model_id': record.id,
                            }
                        )

                        transient_ids.append(transient.id)

                return {'domain': {'many2many_value': [('id', 'in', transient_ids)]}}

    @api.multi
    def edit(self):

        context = {
            'default_name': self.name,
            'default_rule_generator_id': self.rule_generator_id.id,
            'default_rule_model': self.env.context.get('rule_model_id', False),
            'default_rule_field': self.rule_field.id,
            'default_logical_operator': self.logical_operator.id,
            'edit': True,
            'rule_id': self.id,
        }

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

        elif self.fields_type in ['many2many', 'many2one', 'selection']:
            pass

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'rule.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }

    @api.multi
    def create_rule(self):

        rule_model_id = self.env.context.get('rule_model_id', False)

        rule = {
            'generator_id': self.rule_generator_id,
            'rule_model': rule_model_id,
            'rule_field': self.rule_field.id,
            'logical_operator': self.logical_operator.id,
            'fields_type': self.fields_type,
        }

        fields_type = self.fields_type

        if fields_type == 'date':
            rule['date_value'] = self.date_value
            rule['selected_value'] = self.date_value

        elif fields_type == 'datetime':
            rule['datetime'] = self.date_time_value
            rule['selected_value'] = self.date_time_value

        elif fields_type == 'integer':
            rule['integer_value'] = str(self.integer_value)
            rule['selected_value'] = str(self.integer_value)

        elif fields_type == 'boolean':
            rule['bool_value'] = self.bool_value
            rule['selected_value'] = "Verdadero" if self.bool_value else "Falso"

        elif fields_type == 'char':
            rule['char_value'] = self.char_value
            rule['selected_value'] = self.char_value

        elif fields_type in ['float', 'monetary']:
            rule['float_value'] = str(self.float_value)
            rule['selected_value'] = str(self.float_value)

        elif fields_type in [' many2many', 'many2one', 'selection']:
            rule['many2many_value'] = str(self.many2many_value)
            rule['selected_value'] = self.many2many_value.name

        else:
            return False
        # programar error

        if self.env.context.get('create', False):
            self.env['rule'].create(rule)

        if self.env.context.get('edit', False):
            self.env['rule'].browse(
                self.env.context.get('rule_id', False)
            ).write(rule)
