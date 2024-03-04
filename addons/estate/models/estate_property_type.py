from odoo import _, api, fields, models


class RealEstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("name_uniq", "unique (name)", _("Property type name already exists!")),
    ]

    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer(default=1)

    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
