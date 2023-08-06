from odoo import api, fields, models


class Product(models.Model):
    _inherit = "product.product"
    _sql_constraints = [
        (
            "default_code_uniq",
            "unique (default_code)",
            "The product code must be unique !",
        ),
    ]

    showed_name = fields.Char(
        string="Name",
        compute="_compute_showed_name",
        translate=True,
        store=True,
    )

    @api.model
    def name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):

        if name:
            if args:
                new_args = [
                    "&",
                    "|",
                    ("showed_name", operator, name),
                    ("default_code", operator, name),
                ] + args
            else:
                new_args = [
                    "|",
                    ("showed_name", operator, name),
                    ("default_code", operator, name),
                ]
            records = self.env["product.product"].search(new_args, limit=limit)
            return models.lazy_name_get(records)
        else:
            return super()._name_search(
                name=name,
                args=args,
                operator=operator,
                limit=limit,
                name_get_uid=name_get_uid,
            )

    # TAKE IN MIND: We are overwriting this method from product_product without
    # calling super().
    # https://github.com/odoo/odoo/blob/12.0/addons/product/models/product.py#L424
    @api.multi
    def name_get(self):
        data = []
        for product in self:
            data.append((product.id, product.showed_name))
        return data

    @api.depends("name", "attribute_value_ids")
    def _compute_showed_name(self):
        for product in self:
            product.showed_name = "{product_name} {variants_attributes}".format(
                product_name=product.name,
                variants_attributes=product._variants_attributes()
            )

    def _variants_attributes(self):
        return self.attribute_value_ids.mapped("name")
