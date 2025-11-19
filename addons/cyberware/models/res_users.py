# -*- coding: utf-8 -*-

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"
    _description = "Extension cyberware des utilisateurs"

    est_charcudoc = fields.Boolean("Charcudoc ?")
    est_client_cyberware = fields.Boolean("Client cyberware ?")

    client_cyberware_ids = fields.One2many(
        "cyberware.client",
        "user_id",
        string="Fiches client liées",
    )
