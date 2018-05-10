# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import itertools
from datetime import datetime

try:
    import xlrd
    try:
        from xlrd import xlsx
    except ImportError:
        xlsx = None
except ImportError:
    xlrd = xlsx = None

class LineImport(models.TransientModel):
    _name = 'import.product.line'
    _description = 'Import Product Line'

    data_file = fields.Binary(string='Product File', required=True,)
    filename = fields.Char()

    @api.multi
    def import_file(self):
        self.ensure_one()
        book = xlrd.open_workbook(file_contents=base64.b64decode(self.data_file))
        sheet = book.sheet_by_index(0)
        data_list = [(row[0].value, row[1].value) for row in itertools.imap(sheet.row, range(sheet.nrows))]

        Product         = self.env['product.product']
        active_id       = self._context.get('active_id', False)
        active_model    = self._context.get('active_model', False)

        # Mua hang
        # Ravi Krishnan - change default_code to name
        if active_model == 'purchase.order':
            PurchaseLine = self.env['purchase.order.line']
            for line in data_list:
                product_id = Product.search([('name','=',line[0])],limit=1)
                po_line_id = PurchaseLine.create({
                    'order_id': active_id,
                    'name': product_id.name,
                    'product_id': product_id.id,
                    'product_uom': product_id.uom_po_id.id,
                    'price_unit': 0,
                    'product_qty': 1,
                    'date_planned': datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                })
                po_line_id.onchange_product_id()
                po_line_id.product_qty = int(line[1])

        # Ravi Krishnan - purchase requisition
        if active_model == 'purchase.requisition':
            PurchaseReqLine = self.env['purchase.requisition.line']
            for line in data_list:
                product_id = Product.search([('name','=',line[0])],limit=1)
                pa_line_id = PurchaseReqLine.create({
                    'requisition_id': active_id,
                    'product_id': product_id.id,
                    'product_uom_id': product_id.uom_po_id.id,
                    'product_qty': 1,
                })
                pa_line_id.product_qty = int(line[1])

        # Chuyen kho
        if active_model == 'stock.picking':        
            picking = self.env['stock.picking'].browse(active_id)
            Move = self.env['stock.move']
            for line in data_list:
                product_id = Product.search([('default_code','=',line[0])],limit=1)
                move = Move.new({
                    'product_id': product_id.id,                     
                    'location_id': picking.location_id.id, 
                    'location_dest_id': picking.location_dest_id.id,
                })
                move.onchange_product_id()
                move_values = move._convert_to_write(move._cache)
                move_values.update({
                    'picking_id': active_id,
                    'product_uom_qty': int(line[1]),
                })
            Move.create(move_values)

        if active_model == 'stock.inventory':
            inventory = self.env['stock.inventory'].browse(active_id)
            InventoryLine = self.env['stock.inventory.line']
            for line in data_list:
                product_id = Product.search([('default_code','=',line[0])],limit=1)
                InventoryLine.create({
                    'inventory_id': active_id,
                    'product_id': product_id.id,
                    'product_uom_id': product_id.uom_id.id,
                    'location_id': inventory.location_id.id,
                    'product_qty': int(line[1]),
                })

        if active_model == 'sale.order':
            SaleOrderLine = self.env['sale.order.line']
            for line in data_list:
                product_id = Product.search([('default_code','=',line[0])],limit=1)
                so_line_id = SaleOrderLine.create({
                    'order_id': active_id,
                    'product_id': product_id.id,
                    'name': product_id.name,
                    'price_unit': 0,
                    'product_qty': 1,
                })
                so_line_id.product_id_change()
                so_line_id.product_uom_qty = int(line[1])

        if active_model == 'account.invoice':
            inv = self.env['account.invoice'].browse(active_id)
            InvoiceLine = self.env['account.invoice.line']
            ctx = {'journal_id': inv.journal_id.id}
            for line in data_list:
                product_id = Product.search([('default_code','=',line[0])],limit=1)
                inv_line_id = InvoiceLine.with_context(ctx).create({
                    'invoice_id': active_id,
                    'product_id': product_id.id,
                    'name': product_id.name,
                    'price_unit': 0,
                    'quantity': int(line[1]),
                })
                inv_line_id._onchange_product_id()

