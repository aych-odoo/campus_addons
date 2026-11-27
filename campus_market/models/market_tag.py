from odoo import fields, models


class MarketTag(models.Model):
    _name = "market.tag"
    _description = "Marketplace Tag"

    name = fields.Char(required=True)

    _name_uniq = models.Constraint(
        "UNIQUE(name)",
        "A tag with this name already exists.",
    )
