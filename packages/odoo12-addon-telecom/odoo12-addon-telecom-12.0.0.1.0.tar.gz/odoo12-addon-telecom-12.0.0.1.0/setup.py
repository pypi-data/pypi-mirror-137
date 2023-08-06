import setuptools

setuptools.setup(
    setup_requires=["setuptools-odoo"],
    odoo_addon={
        "depends_override": {
            "account_payment_order": "odoo12-addon-account-payment-order==12.0.2.0.0.99.dev3", # noqa
            "product_contract": "odoo12-addon-product-contract==12.0.5.2.1",
         },
        "external_dependencies_override": {
            "python": {
                "stdnum": "python-stdnum==1.14",
            },
        },
    },
)
