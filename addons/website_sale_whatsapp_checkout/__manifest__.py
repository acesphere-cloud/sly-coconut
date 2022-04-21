# -*- coding: utf-8 -*-
{
    'name': "Website Sale WhatsApp Checkout",

    'summary': """Now no need to bother for Quotation & Invoice use WhatsApp Checkout""",

    'description': """Now the time to order and checkout via WhatsApp, Now no need to bother for Quotation & Invoice""",

    'author': 'ErpMstar Solutions',
    'category': 'Website',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['website_sale'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'data/sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'images': ['static/description/banner.jpg'],
    'application': True,
    'installable': True,
    'website': '',
    'auto_install': False,
    'price': 40,
    'currency': 'EUR',
}
