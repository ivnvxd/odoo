from odoo import _, fields, models


class RealEstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("name_uniq", "unique (name)", _("Property type name already exists!")),
    ]

    property_ids = fields.One2many("estate.property", "property_type_id")
