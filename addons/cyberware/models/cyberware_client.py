# -*- coding: utf-8 -*-

from datetime import date

from odoo import models, fields, api


class CyberwareClient(models.Model):
    _name = "cyberware.client"
    _description = "Client équipé de cyberware"
    _order = "nom_client"

    actif = fields.Boolean("Actif ?", default=True)

    nom_client = fields.Char("Nom du client", required=True)
    pseudo = fields.Char("Pseudo / alias")
    date_naissance = fields.Date("Date de naissance")

    image_client = fields.Binary("Avatar")

    niveau_essence_max = fields.Integer(
        "Essence maximale",
        default=100,
        help="Limite théorique d'essence / humanité pour ce client.",
    )

    # Lien avec un utilisateur Odoo (pour les groupes client / login portail plus tard si tu veux)
    user_id = fields.Many2one(
        "res.users",
        string="Utilisateur lié",
    )

    # Relations
    implantation_ids = fields.One2many(
        "cyberware.implantation",
        "client_id",
        string="Historique des implantations",
    )

    implant_ids = fields.Many2many(
        "cyberware.implant",
        "cyberware_client_implant_rel",
        "client_id",
        "implant_id",
        string="Implants installés",
        help="Implants actuellement présents chez le client.",
    )

    # Champs calculés
    age = fields.Integer(
        "Âge",
        compute="_compute_age",
        store=True,
    )

    essence_utilisee = fields.Integer(
        "Essence utilisée",
        compute="_compute_essence_utilisee",
        store=True,
    )

    essence_restante = fields.Integer(
        "Essence restante",
        compute="_compute_essence_restante",
        store=True,
    )

    @api.depends("date_naissance")
    def _compute_age(self):
        for client in self:
            if client.date_naissance:
                aujourd_hui = date.today()
                client.age = (
                    aujourd_hui.year
                    - client.date_naissance.year
                    - (
                        (aujourd_hui.month, aujourd_hui.day)
                        < (client.date_naissance.month, client.date_naissance.day)
                    )
                )
            else:
                client.age = 0

    @api.depends("implantation_ids", "implantation_ids.implant_id", "implantation_ids.implant_id.cout_essence")
    def _compute_essence_utilisee(self):
        for client in self:
            essence_totale = 0
            for intervention in client.implantation_ids:
                essence_totale += intervention.implant_id.cout_essence or 0
            client.essence_utilisee = essence_totale

    @api.depends("niveau_essence_max", "essence_utilisee")
    def _compute_essence_restante(self):
        for client in self:
            if client.niveau_essence_max:
                client.essence_restante = client.niveau_essence_max - (client.essence_utilisee or 0)
            else:
                client.essence_restante = 0
