from odoo import fields, models


class MarketOffer(models.Model):
    _name = "market.offer"
    _description = "Marketplace Offer"
    _order = "price desc"

    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    price = fields.Float(required=True)
    listing_id = fields.Many2one("market.listing", required=True)
