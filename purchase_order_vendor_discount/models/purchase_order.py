from odoo import models, fields, api


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    global_descent_type = fields.Float(
        string='Global Descent Type',
        related='partner_id.global_descent_type',
        readonly=True,
        digits=(16, 2)
    )


class PurchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    discount_purchase = fields.Float(
        string='Discount (%)',
        compute='_compute_discount_from_order',
        store=True,  # Store the computed value for better performance
        readonly=True,
        digits=(16, 2)
    )

    @api.depends('order_id.global_descent_type')
    def _compute_discount_from_order(self):
        """Compute discount from the order's global descent type"""
        for line in self:
            line.discount_purchase = line.order_id.global_descent_type or 0.0

    @api.depends('product_id', 'price_unit', 'taxes_id', 'discount', 'product_qty')
    def _compute_amount(self):
        """Override amount computation to include discount"""
        for line in self:
            # Apply discount to the base price
            discounted_price = line.price_unit * (1 - (line.discount_purchase or 0.0) / 100.0)

            # Compute taxes on the discounted price
            taxes = line.taxes_id.compute_all(
                discounted_price,
                line.order_id.currency_id,
                line.product_qty,
                product=line.product_id,
                partner=line.order_id.partner_id
            )

            # Update the line amounts
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],

            })