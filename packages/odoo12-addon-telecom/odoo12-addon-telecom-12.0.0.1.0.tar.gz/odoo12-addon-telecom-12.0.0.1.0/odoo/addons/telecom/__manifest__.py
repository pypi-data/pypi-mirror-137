{
    "name": "Vertical Telecom",
    "summary": """""",
    "author": "Coopdevs Treball SCCL",
    "website": "https://coopdevs.org",
    # Categories can be used to filter modules in modules listing. Find full list on:
    # https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    "category": "Telecom flows management",
    "version": "12.0.0.1.0",
    # any module necessary for this one to work correctly
    "depends": [
        "account_payment_order",
        "base",
        "component_event",
        "crm",
        "crm_lead_product",
        "product",
        "product_contract",
        "sale",
        "sale_management",
        "sale_substate",
    ],
    "external_dependencies": {
        "python": [
            "stdnum",
        ],
    },
    # always loaded
    "data": [
        # Module Data
        "data/ir_module_category.xml",
        # Security
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        # Data
        "data/ir_cron.xml",
        "data/previous.provider.csv",
        "data/contract_template.xml",
        "data/product_attribute.xml",
        "data/product_categories.xml", # TODO: delete this after new catalog migration
        "data/product_category.xml",
        "data/product_template.xml",
        "data/res_company.xml",
        "data/service_supplier.xml",
        "data/service_technology.xml",
        # Views
        "views/sale_order.xml",
        "views/contract.xml",
        "views/crm_lead_line.xml",
        "views/crm_lead.xml",
        "views/product_product.xml",
        "views/product_template.xml",
        "views/res_config_settings.xml",
        "views/base_substate_type.xml",
        "views/base_substate.xml",
        # Menu
        "views/menu.xml",
        # Wizards
        "wizards/crm_lead_line_creation/crm_lead_line_creation_view.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
    ],
}
