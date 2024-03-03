from odoo import _, fields, models


class RealEstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("name_uniq", "unique (name)", _("Property tag name already exists!")),
    ]

    color = fields.Integer()
