from odoo import models, fields
import io
import pandas as pd
import base64

class ExcelUpload(models.Model):
    _name = 'supplier.quotation.excel.upload.model'
    _description = 'Excel Upload'

    name = fields.Char('Name')
    file = fields.Binary('Excel File')
    data = fields.Text('Data')

    def upload_excel(self):

        Product = self.env['product.model']
        Quotation = self.env['quotation.model']
        Supplier = self.env['supplier.model']

        for record in self:
            if record.file:
                try:
                    file_content = io.BytesIO(base64.b64decode(record.file))
                    xls = pd.ExcelFile(file_content)
                except (ValueError, pd.errors.ParserError) as e:
                    raise ValueError("Error parsing the Excel file: {}".format(str(e)))

                for sheet_name in xls.sheet_names:
                    df = xls.parse(sheet_name)

                    file_name = record.name.split(".xlsx")[0].lower()
                    # Determine the mapping based on the file name
                    if file_name == 'cravings':
                        mpn_column = 'Sku'
                        description_column = 'ProductName'
                        price_column = 'Offer'
                        available_units_column = 'QTY'
                    elif file_name == 'newegg':
                        # mpn_column = 'Parts#' if 'Parts#' in df.columns else
                        mpn_column = None
                        if 'Parts#' in df.columns:
                            mpn_column = 'Parts#'
                        if mpn_column is None and 'Lenovo Sku#' in df.columns:
                            mpn_column = 'Lenovo Sku#'
                        print(sheet_name)
                        print(df.keys())
                        assert mpn_column is not None
                        description_column = 'WebDescription' if 'WebDescription' in df.columns else \
                            'Item Description' if 'Item Description' in df.columns else 'Description'
                        price_column = 'Offer price' if 'Offer price' in df.columns else \
                            'Bulk Price' if 'Bulk Price' in df.columns else 'Take Some Price'
                        available_units_column = 'Qty' if 'Qty' in df.columns else 'Inventory'
                    elif file_name == 'tds':
                        mpn_column = 'MFG Part#'
                        description_column = 'Long Description'
                        price_column = 'Price Rebate applied'
                        available_units_column = 'In Stock'
                    elif file_name == 'unavis':
                        mpn_column = 'Model'
                        description_column = 'Description'
                        price_column = 'Price'
                        available_units_column = 'Qty'
                    else:
                        raise ValueError("Unable to find mapping for the given supplier")

                    for _, row in df.iterrows():
                        mpn = row[mpn_column]
                        description = row[description_column]
                        price = row[price_column]
                        available_units = row[available_units_column]

                        # Search for existing product based on mpn
                        product = Product.search([('mpn', '=', mpn)], limit=1)
                        # Find the supplier based on the record name
                        supplier = Supplier.search([('name', '=', file_name)], limit=1)

                        if not product:
                            try:
                                # Create a new product and quotation
                                product = Product.create({
                                    'mpn': mpn,
                                    'description': description,
                                })
                                quotation = Quotation.create({
                                    'supplier_id': supplier.id,
                                    'product_id': product.id,
                                    'price': price,
                                    'available_units': available_units,
                                })
                                # Add the quotation to the product's quotation_ids
                                product.write({'quotation_ids': [(4, quotation.id)]})
                            except Exception as e:
                                raise ValueError("Error creating a new product and quotation: {}".format(str(e)))
                        else:
                            try:
                                # Update existing product and add new quotation
                                quotation = Quotation.create({
                                    'supplier_id': supplier.id,
                                    'product_id': product.id,
                                    'price': price,
                                    'available_units': available_units,
                                })
                                # Add the quotation to the product's quotation_ids
                                product.write({'quotation_ids': [(4, quotation.id)]})
                            except Exception as e:
                                raise ValueError(
                                    "Error updating existing product and adding a new quotation: {}".format(str(e)))


