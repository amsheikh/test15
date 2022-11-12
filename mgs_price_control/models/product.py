from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # maximum_price = fields.Float(string='Maximum Price')
    minimum_price = fields.Float(string='Minimum Price')
