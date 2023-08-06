from odoo import models, fields, api


class CRMLeadLineCreationWizard(models.TransientModel):
    _name = "crm.lead.line.creation.wizard"

    lead_id = fields.Many2one("crm.lead")
    product_template_id = fields.Many2one(
        "product.template",
        "Product Template",
        domain=[
            ("main", "=", True),
            ("type", "=", "telecom_service_recurring")
        ]
    )
    product_id = fields.Many2one(
        "product.product",
        "Product",
    )
    service_street = fields.Char(string="Service Street")
    phone_number = fields.Char(string="Phone Number")

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults["lead_id"] = self.env.context["active_id"]
        return defaults

    @api.onchange("product_template_id")
    def _onchange_product_template_id(self):
        self.product_id = False
        self.service_street = False

    def button_creation(self):
        if self.product_template_id.categ_id == self.env.ref("telecom.mobile_product_category"):
            mobile_isp_info_args = {
                "phone_number": self.phone_number,
            }
            isp_info = self.env["mobile.isp.info"].create(mobile_isp_info_args)
        elif self.product_template_id.categ_id == self.env.ref("telecom.broadband_product_category"):
            broadband_isp_info_args = {
                "service_street": self.service_street,
            }
            isp_info = self.env["broadband.isp.info"].create(broadband_isp_info_args)
        elif self.product_template_id.categ_id == self.env.ref("telecom.landline_product_category"):
            landline_isp_info_args = {
                "service_street": self.service_street,
                "phone_number": self.phone_number,
            }
            isp_info = self.env["landline.isp.info"].create(landline_isp_info_args)
        else:
            # TODO: Create custom exception
            raise Exception()

        lead_line_args = {
            "name": self.product_id.name,
            "lead_id": self.lead_id.id,
            "product_id": self.product_id.id,
            "product_tmpl_id": self.product_id.product_tmpl_id.id,
            "category_id": self.product_id.categ_id.id,
            "isp_info": "%s,%s" % (isp_info._name, isp_info.id),
        }

        self.env["crm.lead.line"].create(lead_line_args)
