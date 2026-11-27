from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class MarketOffer(models.Model):
    _name = "market.offer"
    _description = "Marketplace Offer"
    _order = "price desc"

    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    price = fields.Float(required=True)
    listing_id = fields.Many2one("market.listing", required=True)

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive.",
    )

    @api.constrains("price", "listing_id")
    def _check_offer(self):
        for offer in self:
            if offer.listing_id.state != "available":
                raise ValidationError(self.env._("You cannot make an offer on a listing that is no longer available."))
            if offer.partner_id == offer.listing_id.seller_id.partner_id:
                raise ValidationError(self.env._("You cannot make an offer on your own listing."))
            if not offer.listing_id.is_negotiable and offer.price < offer.listing_id.price:
                raise ValidationError(self.env._("This listing is not negotiable: the offer must be at least the asking price."))

    def action_accept(self):
        for offer in self:
            if offer.listing_id.state != "available":
                raise UserError(self.env._("Only available listings can be sold."))
            offer.listing_id.write({
                "state": "sold",
                "buyer_id": offer.partner_id.id,
                "selling_price": offer.price,
            })

    def action_refuse(self):
        self.unlink()
