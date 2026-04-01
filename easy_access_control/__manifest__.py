{
    'name': 'Easy Access Control',
    'version': '16.0.1.1',  # 🔥 version change (cache fix)

    'summary': 'Control user access (Create, Edit, Delete) easily in Odoo',

    'description': """
Easy Access Control

A simple and powerful module to control user permissions at model level.

Features:
- Block Create action
- Block Edit action
- Block Delete action
- User-based access control
- Model-level restriction
- Easy configuration

Improve your data safety and prevent unwanted changes in your Odoo system.
""",

    'author': 'Mohan Mathanabalan',
    'website': 'https://github.com/mailtomemohan9387/easy_access_control',

    'category': 'Extra Tools',
    'license': 'LGPL-3',

    'depends': ['base', 'contacts'],

    'data': [
        'security/ir.model.access.csv',
        'views/access_manager_views.xml',
    ],

    # ✅ Cover image (IMPORTANT)
    'images': [
        'static/description/banner.png',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,

    'price': 49.0,
    'currency': 'USD',
}
