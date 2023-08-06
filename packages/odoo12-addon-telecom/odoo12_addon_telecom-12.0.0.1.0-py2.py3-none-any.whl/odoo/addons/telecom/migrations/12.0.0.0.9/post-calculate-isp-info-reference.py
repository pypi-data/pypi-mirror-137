# ISP INFO
# Telecom X.Y.Z: CRMLeadLine, SaleOrder y Contract apuntan a mobile_isp_info y broadband_isp_info y tienen que apuntar a isp_info
#   - Post: Mover la referencia del isp_info de la col temporal a la columna `isp_info`
import logging

_logger = logging.getLogger(__name__)


def update_isp_info(cr, table):
    cr.execute('SELECT id, temporary_isp_info FROM {} WHERE temporary_isp_info IS NOT NULL'.format(table))
    records = cr.dictfetchall()

    for record in records:
        _logger.info("START: {}, {}".format(table, record))
        cr.execute("UPDATE {} SET isp_info='{}' WHERE id = {}".format(table, record["temporary_isp_info"], record["id"]))
        _logger.info("UPDATED: {} with {}".format(record, record["temporary_isp_info"]))

    cr.execute('ALTER TABLE {} DROP COLUMN temporary_isp_info'.format(table))

def migrate(cr, version):
    update_isp_info(cr, "crm_lead_line")
    update_isp_info(cr, "sale_order")
    update_isp_info(cr, "contract_contract")
