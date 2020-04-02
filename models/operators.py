# -*- coding: utf-8 -*-

from openerp import models, fields, api


class OperatorFields(models.Model):
    _name = 'operator.fields'
    _description = 'Operator Fields'

    name = fields.Char()

class LogicalOperators(models.Model):
    _name = 'logical.operators'
    _description = 'Logical Operators'

    name = fields.Char(
        string='Nombre',
    )

    symbol = fields.Char(
        string='Símbolo',
    )