from odoo import models, fields

class Supplier(models.Model):
    _name = 'supplier.model'
    _description = 'Supplier Model'

    name = fields.Selection([
        ('cravings', 'cravings'),
        ('newegg', 'newegg'),
        ('tds', 'tds'),
        ('unavis', 'unavis')
    ], string='Supplier Name')
    details = fields.Text(string='Details')

    quotation_ids = fields.One2many('quotation.model', 'supplier_id', string='Quotations')

