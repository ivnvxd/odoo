from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class RealEstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = fields.Date.today() + timedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            accepted_offers = record.property_id.offer_ids.filtered(
                lambda x: x.status == "accepted" and x.id != record.id
            )
            if accepted_offers:
                raise UserError(_("Another offer has already been accepted"))
            else:
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id.id
                record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            record.status = "refused"

    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price > 0)",
            _("The price of the offer must be positive."),
        ),
    ]

    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
