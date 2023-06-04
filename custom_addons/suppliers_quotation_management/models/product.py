from odoo import models, fields

class Product(models.Model):
    _name = 'product.model'
    _description = 'Product Model'

    mpn = fields.Char(string='MPN', required=True)
    brand = fields.Char(string='Brand')
    description = fields.Text(string='Description')
    quotation_ids = fields.One2many('quotation.model', 'product_id', string='Quotations')
    supplier_ids = fields.Many2many('supplier.model', string='Suppliers')

