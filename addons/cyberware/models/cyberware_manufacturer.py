from odoo import models, fields

class Manufacturer(models.Model):
    _name = 'cyberware.manufacturer'
    _description = 'Juste pour la consigne'

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    manufacturer_id = fields.Many2one('cyberware.manufacturer', string="Fabricant")