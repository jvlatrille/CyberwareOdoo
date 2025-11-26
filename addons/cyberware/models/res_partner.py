# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'  # On étend le modèle existant

    # On ajoute nos champs spécifiques
    is_charcudoc = fields.Boolean(string="Est un Charcudoc", default=False)
    
    # Optionnel : Une spécialité pour le RP
    charcudoc_speciality = fields.Selection([
        ('generalist', 'Généraliste'),
        ('implants', 'Implants Militaires'),
        ('cosmetic', 'Bioplastie / Cosmétique')
    ], string="Spécialité")