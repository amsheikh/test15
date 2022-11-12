from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # maximum_price = fields.Float(
    #     default=0.0, compute='_compute_maximum_minimum_price')
    minimum_price = fields.Float(
        default=0.0, compute='_compute_maximum_minimum_price')

    @api.depends('product_id')
    def _compute_maximum_minimum_price(self):
        for r in self:
            r.minimum_price = 0
            if r.product_id:
                # r.maximum_price = r.product_id.product_tmpl_id.maximum_price or r.product_id.list_price
                r.minimum_price = r.product_id.product_tmpl_id.minimum_price or r.product_id.standard_price

    @api.constrains('price_unit', 'minimum_price')
    def compare_price_units(self):
        # @api.onchange('price_unit')
        # def compare_price_units(self):
        for r in self:
            product_id = self.env['product.product'].search(
                [('id', '=', r.product_id.id)], limit=1)
            # maximum_price = product_id.product_tmpl_id.maximum_price or product_id.list_price
            minimum_price = product_id.product_tmpl_id.minimum_price or product_id.standard_price

            if not self.env.user.has_group('mgs_price_control.minimum_maximum_confirm') and r.price_unit < minimum_price and r.product_id.detailed_type == 'product':
                raise UserError(
                    "Sale price of the %s should be greater than %s" % (product_id.name, minimum_price))

    @api.constrains('product_uom_qty')
    def check_item_qty_available(self):
        # @api.onchange('price_unit')
        # def compare_price_units(self):
        for r in self:
            ordered_qty = r.product_uom_qty - r.qty_delivered
            if not self.env.user.has_group('mgs_price_control.minimum_qty_confirm') and ordered_qty > r.free_qty_today and r.product_id.detailed_type == 'product':
                raise UserError("""You're trying to sell %s% s of the product %s which you don't have
Available Quantity: %s %s""" % (ordered_qty, r.product_uom.name, r.product_id.name, r.free_qty_today, r.product_uom.name))
