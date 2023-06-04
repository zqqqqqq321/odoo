from odoo import models, fields

class Quotation(models.Model):
    _name = 'quotation.model'
    _description = 'Quotation Model'

    supplier_id = fields.Many2one('supplier.model', string='Supplier')
    product_id = fields.Many2one('product.model', string='Product')
    price = fields.Float(string='Quoted Price')
    available_units = fields.Integer(string='Available Units')
    quotation_date = fields.Date(string='Quotation Date')
