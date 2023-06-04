from odoo import models, fields

class Supplier(models.Model):
    _name = 'supplier.model'
    _description = 'Supplier Model'

    name = fields.Selection([
        ('cravings', 'Cravings'),
        ('Newegg', 'Newegg'),
        ('tds', 'TDS'),
        ('unavis', 'Unavis')
    ], string='Supplier Name')

    quotation_ids = fields.One2many('quotation.model', 'supplier_id', string='Quotations')

