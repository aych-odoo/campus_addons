from odoo import fields, models


class MarketListing(models.Model):
    _name = "market.listing"
    _description = "Marketplace Listing"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    price = fields.Float(string="Asking Price", required=True)
    condition = fields.Selection([
        ("new", "New"),
        ("like_new", "Like New"),
        ("used", "Used"),
    ])
    is_negotiable = fields.Boolean(string="Negotiable")
    image = fields.Image(max_width=1024, max_height=1024)
    category_id = fields.Many2one("market.category")
