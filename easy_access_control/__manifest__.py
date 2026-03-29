{
    'name': 'Easy Access Control',
    'version': '16.0.1.0.0',
    'summary': 'Simple user access control manager',
    'author': 'Mohan Mathanabalan',
    'category': 'Tools',
    'depends': ['base', 'contacts'],
    'price': 63.00,
    'currency': 'USD',
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/access_manager_views.xml',
    ],
    'installable': True,
    'application': True,
}
