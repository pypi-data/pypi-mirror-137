from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    start_provisioning_crm_stage = fields.Many2one(
        related="company_id.start_provisioning_crm_stage",
        string="Start provisioning CRM stage",
        readonly=False,
    )
