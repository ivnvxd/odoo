from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class RealEstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,
        default=lambda self: fields.Date.today() + timedelta(days=90),
        string="Available From",
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
        required=True,
        copy=False,
        string="Status",
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesman_id = fields.Many2one("res.users", string="Salesman")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(
        compute="_compute_total_area", string="Total Area (sqm)"
    )
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_sold(self):
        if self.state == "canceled":
            raise UserError(_("Canceled properties cannot be sold."))
        else:
            self.state = "sold"
        return True

    def action_cancel(self):
        if self.state == "sold":
            raise UserError(_("Sold properties cannot be canceled."))
        else:
            self.state = "canceled"
        return True

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            _("The expected price must be positive"),
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            _("The selling price must be positive"),
        ),
    ]

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                min_price = record.expected_price * 0.9
                if (
                    float_compare(record.selling_price, min_price, precision_digits=2)
                    == -1
                ):
                    raise ValidationError(
                        _(
                            "Selling price must be at least 90% of the expected price. You must reduce the expected price if you want to accept this offer."
                        )
                    )

    @api.ondelete(at_uninstall=False)
    def _ondelete(self):
        for record in self:
            if record.state not in ["new", "canceled"]:
                raise UserError(_("Only new and canceled properties can be deleted."))
