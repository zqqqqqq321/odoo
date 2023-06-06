from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Quotation(models.Model):
    _name = 'quotation.model'
    _description = 'Quotation Model'

    supplier_id = fields.Many2one('supplier.model', string='Supplier')
    product_id = fields.Many2one('product.model', string='Product')
    price = fields.Float(string='Quoted Price')
    available_units = fields.Integer(string='Available Units')
    quotation_date = fields.Datetime(string='Quotation Date', default=fields.Datetime.now)

    @api.constrains('price')
    def _check_price(self):
        for quotation in self:
            # Error check: Ensure that the price is not negative
            if quotation.price < 0.0:
                raise ValidationError("Price cannot be negative.")

    @api.constrains('available_units')
    def _check_available_units(self):
        for quotation in self:
            # Error check: Ensure that the available units is not negative
            if quotation.available_units < 0:
                raise ValidationError("Available units cannot be negative.")
