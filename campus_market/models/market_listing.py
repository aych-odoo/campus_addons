from odoo import fields, models


class MarketListing(models.Model):
    _name = "market.listing"
    _description = "Marketplace Listing"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    price = fields.Float(string="Asking Price", required=True)
