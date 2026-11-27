from odoo import api, fields, models


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
    tag_ids = fields.Many2many("market.tag")
    seller_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    offer_ids = fields.One2many("market.offer", "listing_id")
    best_offer = fields.Float(compute="_compute_best_offer")

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The asking price must be strictly positive.",
    )

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for listing in self:
            listing.best_offer = max(listing.offer_ids.mapped("price"), default=0.0)
