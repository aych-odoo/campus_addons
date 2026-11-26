from odoo import fields, models


class MarketCategory(models.Model):
    _name = "market.category"
    _description = "Marketplace Category"

    name = fields.Char(required=True)
