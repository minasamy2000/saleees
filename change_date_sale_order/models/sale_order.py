
from odoo import models, fields, api


class change_date_sale_order(models.Model):
    _inherit = 'sale.order'

    def _prepare_confirmation_values(self):
        """ Prepare the sales order confirmation values.

        Note: self can contain multiple records.

        :return: Sales Order confirmation values
        :rtype: dict
        """
        return {
            'state': 'sale',
        }




