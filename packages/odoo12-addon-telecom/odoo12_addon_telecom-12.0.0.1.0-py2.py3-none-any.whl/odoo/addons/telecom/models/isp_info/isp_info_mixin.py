from odoo import models, fields


class ISPInfoMixin(models.AbstractModel):
    _name = 'isp.info.mixin'
    _description = 'ISP Info mixin'

    isp_info = fields.Reference(
        selection=[
            ('mobile.isp.info','mobile.isp.info'),
            ('broadband.isp.info','broadband.isp.info'),
            ('landline.isp.info','landline.isp.info'),
        ]
    )
