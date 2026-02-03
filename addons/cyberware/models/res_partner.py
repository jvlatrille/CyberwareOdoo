# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'  # On étend le modèle existant

    # Ajout du champ spécifique
    is_charcudoc = fields.Boolean(string="Est un Charcudoc", default=False)
    
    # Avec une spécialité (a selecionner)
    charcudoc_speciality = fields.Selection([
        ('generalist', 'Généraliste'),
        ('implants', 'Implants Militaires'),
        ('cosmetic', 'Bioplastie / Cosmétique')
    ], string="Spécialité")