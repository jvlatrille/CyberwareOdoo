# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CyberwareImplant(models.Model):
    _name = "cyberware.implant"
    _description = "Implants cyberware"
    _order = "rarete, nom_implant"

    actif = fields.Boolean("Actif ?", default=True)

    nom_implant = fields.Char("Nom de l'implant", required=True)
    description = fields.Text("Description")
    type_implant = fields.Selection(
        [
            ("optique", "Optique"),
            ("neural", "Neural"),
            ("armure", "Armure"),
            ("membre", "Membre cybernétique"),
            ("interne", "Organe interne"),
        ],
        string="Type d'implant",
        required=True,
    )
    rarete = fields.Selection(
        [
            ("commun", "Commun"),
            ("rare", "Rare"),
            ("epique", "Épique"),
            ("légendaire", "Légendaire"),
        ],
        string="Rareté",
        default="commun",
        required=True,
    )

    prix_euro = fields.Float("Prix (€)")
    cout_essence = fields.Integer("Coût en essence", help="Coût en essence / humanité pour cet implant.")
    emplacement = fields.Selection(
        [
            ("tete", "Tête"),
            ("torse", "Torse"),
            ("bras", "Bras"),
            ("jambes", "Jambes"),
            ("systeme", "Système interne"),
        ],
        string="Emplacement",
    )
    image_implant = fields.Binary("Image")

    # Relations
    charcudoc_id = fields.Many2one(
        "res.users",
        string="Charcudoc créateur",
        default=lambda self: self.env.user,
    )
    implantation_ids = fields.One2many(
        "cyberware.implantation",
        "implant_id",
        string="Interventions",
    )

    # Champ calculé (pour les vues plus tard)
    nb_implantations = fields.Integer(
        "Nombre d'implantations",
        compute="_compute_nb_implantations",
        store=True,
    )

    @api.depends("implantation_ids")
    def _compute_nb_implantations(self):
        for enregistrement in self:
            enregistrement.nb_implantations = len(enregistrement.implantation_ids)
