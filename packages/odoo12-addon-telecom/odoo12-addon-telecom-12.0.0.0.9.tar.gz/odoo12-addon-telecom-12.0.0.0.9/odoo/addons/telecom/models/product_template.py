from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    type = fields.Selection(
        selection_add=[
            ('telecom_service_recurring', 'Telecom Service Recurring'),
            ('telecom_service_one_shot', 'Telecom Service One Shot'),
        ],
    )

    main = fields.Boolean(
        help='Check this field if the product is incompatible with other products with the same template. Eg. GSM 100 minutes and GSM 0 minutes. You can only have one of these products active at the same time.'
    )

    @api.constrains('is_contract', 'type')
    def _check_contract_product_type(self):
        """
        Contract product should be service type
        """
        if self.is_contract and self.type not in ['service', 'telecom_service_recurring']:
            raise ValidationError(_("Contract product should be service or telecom_service_recurring type"))
