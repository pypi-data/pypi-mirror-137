from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MobileISPInfo(models.Model):
    _inherit = "base.isp.info"

    _name = "mobile.isp.info"
    _description = "Mobile ISP Info"
    icc = fields.Char(string="ICC", store=True)
    icc_donor = fields.Char(string="ICC Donor")
    previous_contract_type = fields.Selection(
        [("contract", "Contract"), ("prepaid", "Prepaid")],
        string="Previous Contract Type",
    )

    @api.constrains("type", "icc_donor", "previous_contract_type", "previous_provider")
    def _check_mobile_portability_info(self):
        if self.type == "new":
            return True
        if not self.previous_contract_type:
            raise ValidationError(
                _("Previous contract type is required in a portability")
            )
        if not self.icc_donor and self.previous_contract_type == "prepaid":
            raise ValidationError(_("ICC donor is required in a portability"))
        if not self.previous_provider.mobile:
            raise ValidationError(
                _("This previous provider does not offer mobile services")
            )
