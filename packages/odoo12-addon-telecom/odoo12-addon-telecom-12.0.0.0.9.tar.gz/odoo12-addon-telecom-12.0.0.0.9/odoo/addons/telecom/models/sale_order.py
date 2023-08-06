from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = ["telecom.mixin", "isp.info.mixin", "sale.order"]
    _name = "sale.order"

    product_template_id = fields.Many2one(
        related="product_id.product_tmpl_id"
    )
    product_id = fields.Many2one(
        "product.product",
        compute="_compute_product",
        string="Product",
    )

    def _compute_product(self):
        for order in self:
            if order.order_line:
                order.product_id = order.order_line[0].product_id

    def _get_default_substate_domain(self, state_val=False):
        domain = super(SaleOrder, self)._get_default_substate_domain(state_val)
        domain += [("product_template_ids", "=", self.product_template_id.id)]
        return domain

    def _get_substate_type(self):
        return self.env["base.substate.type"].search(
            [
                ("model", "=", self._name),
                ("product_template_ids", "=", self.product_template_id.id),
            ],
            limit=1,
        )

    @api.constrains("substate_id", "state")
    def check_substate_id_value(self):
        sale_states = dict(self._fields["state"].selection)
        for order in self:
            order_template = order.product_template_id
            substate_templates = (
                order.substate_id.target_state_value_id.base_substate_type_id.product_template_ids # noqa
            )
            target_state = order.substate_id.target_state_value_id.target_state_value
            if order.substate_id and order.state != target_state:
                raise ValidationError(
                    _(
                        "The substate '%s' is not defined for the state"
                        " '%s' but for '%s' "
                    )
                    % (
                        order.substate_id.name,
                        _(sale_states[order.state]),
                        _(sale_states[target_state]),
                    )
                )
            if order.substate_id and order_template not in substate_templates:
                raise ValidationError(
                    _("The substate '%s' is not in '%s'")
                    % (
                        order.substate_id.name,
                        substate_templates,
                    )
                )

    @api.multi
    def _prepare_contract_value(self, contract_template):
        self.ensure_one()
        values = super(SaleOrder, self)._prepare_contract_value(contract_template)
        values.update(
            {
                "isp_info": "%s,%s" % (self.isp_info._name, self.isp_info.id),
            }
        )
        return values
