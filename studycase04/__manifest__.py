# -*- coding: utf-8 -*-
{
    'name': "hotel_booking_order",

    'summary': """
        Booking system untuk kamar hotel.""",

    'description': """
        Description here.
    """,

    'author': "WIR",
    'website': "http://www.wir.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Management',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['account','base','mail'],

    # always loaded
    'data': [
        'security/security_rules.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/kamarhotel_views.xml',
        'views/fasilitas_views.xml',
        'views/transaksi_views.xml',
        'views/tipekamar_views.xml',
        'views/respartner_views.xml',
        'views/team_views.xml',
        'views/master_menu.xml',
        'views/settings_komisi.xml',
        'views/salesreport_views.xml',
         'views/report_invoice.xml',
        'data/sequence_booking.xml',
        'data/email_templates.xml',
        'data/automated_check.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
