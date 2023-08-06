from odoo import models, fields


class LandlineISPInfo(models.Model):
    _inherit = 'base.isp.info'

    _name = 'landline.isp.info'
    _description = "Landline ISP Info"

    service_street = fields.Char(string='Service Street')
