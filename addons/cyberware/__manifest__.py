# -*- coding: utf-8 -*-
{
    'name': "cyberware",

    'summary': "Un module Odoo permettant la gestion d'implants cyberware",

    'description': """
Bla bla bla
    """,

    'author': "VINET LATRILLE Jules",
    'website': "https://www.gamesatlas.com/cyberpunk-2077/cyberware/", # C'est le site sur lequel je me base pour les implants

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Cyberware',
    'version': '18.0.1.0.0',


    # any module necessary for this one to work correctly
    'depends': ['base'],
    'application': True,
    'license': "AGPL-3",
    
    'images': [
        'static/description/icon.png',
    ],
    # always loaded
    'data': [
        # Sécurité
        'security/cyberware_security.xml',
        'security/ir.model.access.csv',

        # Menus + vues backend
        'views/cyberware_actions.xml',
        'views/cyberware_menu.xml',
        'views/cyberware_implant_views.xml',
        'views/cyberware_client_views.xml',
        'views/cyberware_ripperdoc_views.xml',
        'views/res_partner_views.xml',

        # Templates / page web (QWeb)
        'views/cyberware_website_templates.xml',
        
        'demo/cyberware.manufacturer.csv',
        'demo/cyberware.demo.xml',
        'demo/cyberware.client.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}

