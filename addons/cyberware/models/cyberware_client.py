# -*- coding: utf-8 -*-

from datetime import date
from odoo.exceptions import ValidationError
from odoo import models, fields, api


class CyberwareClient(models.Model):
    _name = "cyberware.client"
    _description = "Client équipé de cyberware"
    _order = "nom_client"

    actif = fields.Boolean("Actif ?", default=True)

    notes_medicales = fields.Text("Notes médicales / Allergies")  # Champ TEXTUEL

    niveau_essence_max = fields.Integer(
        "Essence maximale",
        default=100,
        help="Limite théorique d'essence / humanité pour ce client.",
    )  # Champ NUMÉRIQUE

    date_naissance = fields.Date("Date de naissance")  # Champ DATE

    image_client = fields.Binary("Avatar")  # Champ IMAGE

    groupe_sanguin = fields.Selection(
        [
            ("a_pos", "A+"),
            ("a_neg", "A-"),
            ("b_pos", "B+"),
            ("b_neg", "B-"),
            ("o_pos", "O+"),
            ("o_neg", "O-"),
            ("ab_pos", "AB+"),
            ("ab_neg", "AB-"),
            ("synth", "Synthétique"),
        ],
        string="Groupe Sanguin",
        default="o_pos",
    )  # Champ SELECT

    age = fields.Integer(
        "Âge",
        compute="_compute_age",
        store=True,
    )  # Champs calculés

    email_user = fields.Char(
        string="Email (lié au compte)",
        related="user_id.login",
        readonly=True,
        store=True,
    )  # Champ RELATED

    nom_client = fields.Char("Nom du client", required=True)
    pseudo = fields.Char("Pseudo / alias")

    user_id = fields.Many2one(
        "res.users",
        string="Utilisateur lié",
    )

    # Relations
    # RELATION 1-N avec les implantations
    implantation_ids = fields.One2many(
        "cyberware.implantation",
        "client_id",
        string="Historique des implantations",
    )

    # RELATION N-N avec les implants
    implant_ids = fields.Many2many(
        "cyberware.implant",
        "cyberware_client_implant_rel",
        "client_id",
        "implant_id",
        string="Implants installés",
        help="Implants actuellement présents chez le client.",
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

    def action_controler_donnees(self):
        """Vérifie la cohérence des données du patient"""
        for record in self:
            # Vérifier la surcharge
            if record.essence_restante < 0:
                raise ValidationError(
                    "DANGER : Le patient a dépassé sa limite de tolérance (Cyberpsychose imminente) !"
                )

            # Vérifier le groupe sanguin
            if not record.groupe_sanguin:
                raise ValidationError(
                    "Merci de renseigner le groupe sanguin pour compléter le dossier."
                )

        # Si tout est OK, on affiche une notif
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Conforme",
                "message": "Le dossier du patient est valide.",
                "type": "success",
                "sticky": False,
            },
        }

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

    @api.depends(
        "implantation_ids",
        "implantation_ids.implant_id",
        "implantation_ids.implant_id.cout_essence",
    )
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
                client.essence_restante = client.niveau_essence_max - (
                    client.essence_utilisee or 0
                )
            else:
                client.essence_restante = 0
