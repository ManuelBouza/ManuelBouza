# -*- coding: utf-8 -*-
from openerp import models, fields, api


class ruleWizard(models.TransientModel):
    _name = 'rule.wizard'
    _description = 'rule Wizard'
    _inherit = 'rule'

