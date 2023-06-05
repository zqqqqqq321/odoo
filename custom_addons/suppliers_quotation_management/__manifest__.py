# -*- coding: utf-8 -*-
{
    'name': 'Import suppliers quotation from excel',
    'description': "",
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/product_detail_views.xml',
        'security/security.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
