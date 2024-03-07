import logging

from odoo import models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        logging.warning("EstateProperty action_sold called")
        return super().action_sold()
