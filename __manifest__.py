{
    'name': 'Easy Access Control',
    'version': '16.0.1.1',
    'summary': 'Control create, edit, delete, and read access for users in Odoo',

    'description': """
Easy Access Control

A simple and powerful Odoo module to control user permissions at model level.

Main Features:
- Block Create action
- Block Edit action
- Block Delete action
- Block Read access
- User-based access control
- Model-level restriction
- Easy configuration

This module helps improve data safety and prevents unwanted changes in your Odoo system.
""",

    'author': 'Mohan',
    'website': 'https://github.com/mailtomemohan9387/easy_access_control',
    'category': 'Extra Tools',
    'license': 'LGPL-3',

    'depends': ['base', 'contacts'],

    'data': [
        'security/ir.model.access.csv',
        'views/access_manager_views.xml',
    ],

    'images': [
        'static/description/banner.png',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 49.0,
    'currency': 'USD',
}
