# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class CyberwareWebsite(http.Controller):
    
    @http.route('/cyberware/market', auth='public', website=True)
    def index(self, **kw):
        # Récupérer tous les implants
        implants = request.env['cyberware.implant'].search([])
        
        # Rendre le template avec les données
        return request.render('cyberware.cyberware_market_page', {
            'implants': implants
        })