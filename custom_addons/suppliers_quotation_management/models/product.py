from odoo import models, fields, api


class Product(models.Model):
    _name = 'product.model'
    _description = 'Product Model'

    mpn = fields.Char(string='MPN', required=True)
    brand = fields.Char(string='Brand')
    description = fields.Text(string='Description')
    quotation_ids = fields.One2many('quotation.model', 'product_id', string='Quotations')
    minimum_price = fields.Float(string='Minimum Price', compute='_compute_minimum_price')
    last_updated_date = fields.Datetime(string='Last Updated Date', readonly=True)

    name = fields.Char(string='Name', compute='_compute_name')

    @api.depends('mpn')
    def _compute_name(self):
        for product in self:
            product.name = product.mpn
    @api.depends('quotation_ids.price')
    def _compute_minimum_price(self):
        for product in self:
            prices = product.quotation_ids.mapped('price')
            if prices:
                product.minimum_price = min(prices)
            else:
                product.minimum_price = 0.0
            product.last_updated_date = fields.Datetime.now()
