from odoo import models, fields, api


class TelecomMixin(models.AbstractModel):
    _name = 'telecom.mixin'
    _description = 'Telecom mixin'

    is_mobile = fields.Boolean(
        compute="_compute_is_mobile",
#        store=True,
    )
    is_adsl = fields.Boolean(
        compute="_compute_is_adsl",
#        store=True,
    )
    is_fiber = fields.Boolean(
        compute="_compute_is_fiber",
#        store=True,
    )
    is_landline = fields.Boolean(
        compute="_compute_is_landline",
#        store=True,
    )

    @api.depends("product_id")
    def _compute_is_mobile(self):
        mobile = self.env.ref("telecom.gsm_recurring_product_template")
        for record in self:
            record.is_mobile = (
                mobile.id == record.product_id.product_tmpl_id.id
            )

    @api.depends("product_id")
    def _compute_is_adsl(self):
        adsl = self.env.ref("telecom.adsl_recurring_product_template")
        for record in self:
            record.is_adsl = (
                adsl.id == record.product_id.product_tmpl_id.id
            )

    @api.depends("product_id")
    def _compute_is_fiber(self):
        fiber = self.env.ref("telecom.fiber_recurring_product_template")
        for record in self:
            record.is_fiber = (
                fiber.id == record.product_id.product_tmpl_id.id
            )

    @api.depends("product_id")
    def _compute_is_landline(self):
        fiber = self.env.ref("telecom.landline_recurring_product_template")
        for record in self:
            record.is_landline = (
                fiber.id == record.product_id.product_tmpl_id.id
            )

