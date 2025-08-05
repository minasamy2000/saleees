# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    global_descent_type = fields.Float(
        string='Global Descent Type',
        help='Custom float field for descent type',
        digits=(16, 2)  # Optional: specify precision
    )