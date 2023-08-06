from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    start_provisioning_crm_stage = fields.Many2one(
        "crm.stage",
        string="Start provisioning CRM stage",
        ondelete="restrict"
    )
