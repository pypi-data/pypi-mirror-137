from odoo import models, fields, api


class TelecomMixin(models.AbstractModel):
    _name = 'telecom.mixin'
    _description = 'Telecom mixin'

    is_mobile = fields.Boolean(
        compute="_compute_is_mobile",
        store=True,
    )
    is_adsl = fields.Boolean(
        compute="_compute_is_adsl",
        store=True,
    )
    is_fiber = fields.Boolean(
        compute="_compute_is_fiber",
        store=True,
    )
    is_landline = fields.Boolean(
        compute="_compute_is_landline",
        store=True,
    )
    is_radiofrequency = fields.Boolean(
        compute="_compute_is_radiofrequency",
        store=True,
    )
    is_telecom = fields.Boolean(
        compute="_compute_is_telecom",
        store=True,
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
        landline = self.env.ref("telecom.landline_recurring_product_template")
        for record in self:
            record.is_landline = (
                landline.id == record.product_id.product_tmpl_id.id
            )

    @api.depends("product_id")
    def _compute_is_radiofrequency(self):
        radiofrequency = self.env.ref("telecom.radiofrequency_recurring_product_template")
        for record in self:
            record.is_radiofrequency = (
                radiofrequency.id == record.product_id.product_tmpl_id.id
            )

    @api.depends("is_adsl", "is_mobile", "is_fiber", "is_landline", "is_radiofrequency")
    def _compute_is_telecom(self):
        for record in self:
            record.is_telecom = (
                record.is_adsl or
                record.is_mobile or
                record.is_fiber or
                record.is_landline or
                record.is_radiofrequency
            )
