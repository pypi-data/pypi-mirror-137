# ISP INFO
# Telecom X.Y.Z: CRMLeadLine, SaleOrder y Contract apuntan a mobile_isp_info y broadband_isp_info y tienen que apuntar a isp_info
#   - Pre: Calcular la referencia del isp_info (`mobile_isp_info,23`) y guardamos en una col temporal
import logging

_logger = logging.getLogger(__name__)


def update_isp_info(cr, table):
    # Create temporary column to store isp_info reference
    cr.execute('ALTER TABLE {} ADD temporary_isp_info VARCHAR'.format(table))

    cr.execute('SELECT id, mobile_isp_info, broadband_isp_info FROM {}'.format(table))
    records = cr.dictfetchall()

    for record in records:
        _logger.info("START: {}, {}".format(table, record))
        if record["broadband_isp_info"]:
            isp_info_ref = "broadband.isp.info,{}".format(record["broadband_isp_info"])
        elif record["mobile_isp_info"]:
            isp_info_ref = "mobile.isp.info,{}".format(record["mobile_isp_info"])
        else:
            # Exceptions to manually review
            if table == "sale_order" and record["id"] in (270, 283, 284, 290, 295, 299, 318, 321):
                continue
            if table == "contract_contract" and record["id"] in (239, 259, 260, 264, 280, 283, 292):
                continue
            raise Exception()
        cr.execute("UPDATE {} SET temporary_isp_info='{}' WHERE id = {}".format(table, isp_info_ref, record["id"]))
        _logger.info("UPDATED: {} with {}".format(record, isp_info_ref))

def migrate(cr, version):
    update_isp_info(cr, "crm_lead_line")
    update_isp_info(cr, "sale_order")
    update_isp_info(cr, "contract_contract")
