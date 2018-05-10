# -*- coding: utf-8 -*-
{
    'name': 'Import line of SO/PO/DO/Invoice/Inventory Adjustment from Excel file',
    'version': '1.0',
    'summary': 'Import line of SO/PO/DO/Invoice/Inventory Adjustment from Excel file',
    'description': """
Import line of SO/PO/DO/Invoice/Inventory Adjustment from Excel file
    """,
    'author': 'SkyERP',
    'website': 'https://skyerp.net',
    'images': [],
    'depends': ['purchase','sale_stock'],
    'data': [
        'security/data.xml',
        'wizard/import_product_wizard.xml',
        'views/sales_view.xml',
        'views/purchase_view.xml',
        'views/invoice_view.xml',
        'views/picking_view.xml',
        'views/inventory_adjustment_view.xml',
        'views/purchase_tender_view.xml'
    ],     

    "price": 49.00,
    "currency": "EUR",

    'images': ['static/description/main.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
