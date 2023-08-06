from odoo import models, fields


class BaseSubstateType(models.Model):
    _inherit = "base.substate.type"
    product_template_ids = fields.Many2many(
        "product.template",
        string="Product templates",
    )


class TargetStateValue(models.Model):
    _inherit = "target.state.value"


class BaseSubstate(models.Model):
    _inherit = "base.substate"
    product_template_ids = fields.Many2many(
        related="target_state_value_id.base_substate_type_id.product_template_ids"
    )
