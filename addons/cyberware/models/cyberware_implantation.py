# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CyberwareImplantation(models.Model):
    _name = "cyberware.implantation"
    _description = "Intervention d'implantation de cyberware"
    _order = "date_implantation desc"

    actif = fields.Boolean("Actif ?", default=True)

    date_implantation = fields.Datetime(
        "Date d'implantation",
        default=fields.Datetime.now,
        required=True,
    )

    client_id = fields.Many2one(
        "cyberware.client",
        string="Client",
        required=True,
        ondelete="cascade",
    )

    implant_id = fields.Many2one(
        "cyberware.implant",
        string="Implant",
        required=True,
        ondelete="restrict",
    )

    charcudoc_id = fields.Many2one(
        "res.users",
        string="Charcudoc",
        default=lambda self: self.env.user,
        required=True,
    )

    state = fields.Selection(
        [
            ("planifie", "Planifiée"),
            ("en_cours", "En cours"),
            ("terminee", "Terminée"),
            ("annulee", "Annulée"),
        ],
        string="Statut",
        default="planifie",
    )

    # Champs related pour la consigne (vue avec champ related)
    prix_implant = fields.Float(
        "Prix implant (€)",
        related="implant_id.prix_euro",
        store=False,
    )
    rarete_implant = fields.Selection(
        related="implant_id.rarete",
        string="Rareté",
        store=False,
    )
    cout_essence_implant = fields.Integer(
        related="implant_id.cout_essence",
        string="Coût en essence",
        store=False,
    )

    # Contrôle métier : ne pas dépasser l'essence max du client
    @api.constrains("client_id", "implant_id")
    def _check_contrainte_essence(self):
        for intervention in self:
            if not intervention.client_id or not intervention.implant_id:
                continue

            essence_actuelle = intervention.client_id.essence_utilisee or 0
            cout_implant = intervention.implant_id.cout_essence or 0
            essence_apres = essence_actuelle + cout_implant

            limite = intervention.client_id.niveau_essence_max or 0

            if limite and essence_apres > limite:
                raise ValidationError(
                    "Impossible d'implanter '%s' sur %s : essence maximale dépassée (%s / %s)."
                    % (
                        intervention.implant_id.nom_implant,
                        intervention.client_id.nom_client,
                        essence_apres,
                        limite,
                    )
                )
