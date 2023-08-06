from odoo import api, fields, models
from datetime import date


class ContractContract(models.Model):
    _inherit = ["telecom.mixin", "isp.info.mixin", "contract.contract"]
    _name = "contract.contract"

    product_id = fields.Many2one(
        "product.product",
        compute="_compute_product_id",
        store=True,
    )

    @api.depends("contract_line_ids")
    def _compute_product_id(self):
        for record in self:
            line = self.env["contract.line"].search(
                [
                    ("contract_id", "=", record.id),
                    ("product_id.main", "=", True),
                    ("date_start", "<=", date.today().strftime("%Y-%m-%d")),
                    "|",
                    ("date_end", ">", date.today().strftime("%Y-%m-%d")),
                    ("date_end", "=", False),
                ],
                limit=1,
            )

            if line:
                record.product_id = line.product_id.id
