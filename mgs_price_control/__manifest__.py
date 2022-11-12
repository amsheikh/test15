# -*- coding: utf-8 -*-
{
    'name': "MGS Price Control",

    'summary': "",

    'description': "",

    'author': "Meisour Global Solutions",
    'website': "http://www.meisour.com",

    'category': 'Stock',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_stock'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/product.xml',
        'views/sale.xml',
    ]
}
