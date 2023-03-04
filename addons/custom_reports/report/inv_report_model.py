from odoo import api, models
from odoo.exceptions import UserError
from datetime import datetime

class InvReport(models.AbstractModel):
    _name = 'report.custom_reports.report_inv_report'

    def get_quantities_all(self, inv_date, prod_id):
        move_lines = self.env['stock.move.line'].search([
            ('product_id', '=', prod_id),
            ('date', '<=', inv_date)
        ])
        lines_in = move_lines.filtered(
            lambda x:
            x.is_inventory == False and
            x.location_dest_usage == 'internal'
        )
        qty_in = sum(lines_in.mapped('qty_done'))
        lines_out = move_lines.filtered(
            lambda x:
            x.is_inventory == False and
            (x.location_dest_usage == 'supplier' or x.location_dest_usage == 'customer')
        )
        qty_out = sum(lines_out.mapped('qty_done'))
        adj_neg = move_lines.filtered(
            lambda x:
            x.is_inventory == True and
            x.location_dest_usage == 'inventory'
        )
        qty_neg = sum(adj_neg.mapped('qty_done'))
        adj_pos = move_lines.filtered(
            lambda x:
            x.is_inventory == True and
            x.location_dest_usage == 'internal'
        )
        qty_pos = sum(adj_pos.mapped('qty_done'))

        return qty_in + qty_pos - qty_out - qty_neg

    def get_quantities(self, date_beg, date_end, type, prod_id):
        move_lines = self.env['stock.move.line'].search([
            ('product_id', '=', prod_id),
            ('date', '>=', date_beg),
            ('date', '<=', date_end)
        ])
        if type == 'in':
            lines = move_lines.filtered(
                lambda x:
                x.is_inventory == False and
                x.location_dest_usage == 'internal'
            )
            qty = sum(lines.mapped('qty_done'))
            return qty
        elif type == 'out':
            lines = move_lines.filtered(
                lambda x:
                x.is_inventory == False and
                (x.location_dest_usage == 'supplier' or x.location_dest_usage == 'customer')
            )
            qty = sum(lines.mapped('qty_done'))
            return qty
        elif type == 'negative':
            lines = move_lines.filtered(
                lambda x:
                x.is_inventory == True and
                x.location_dest_usage == 'inventory'
            )
            qty = sum(lines.mapped('qty_done'))
            return qty
        elif type == 'positive':
            lines = move_lines.filtered(
                lambda x:
                x.is_inventory == True and
                x.location_dest_usage == 'internal'
            )
            qty = sum(lines.mapped('qty_done'))
            return qty
        else:
            return 0

    def print_inv_report(self, data):
        beg_date = datetime.strptime(data.get('date_start'), '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(data.get('date_stop'), '%Y-%m-%d %H:%M:%S')
        products = self.env['product.product'].search([])
        prod_details = []

        for product in products:
            beg_qty = self.get_quantities_all(beg_date, product.id)
            end_qty = self.get_quantities_all(end_date, product.id)
            in_qty = self.get_quantities(beg_date, end_date, 'in', product.id)
            in_qty = '{:,.0f}'.format(in_qty)
            out_qty = self.get_quantities(beg_date, end_date, 'out', product.id)
            out_qty = '{:,.0f}'.format(out_qty)
            neg_qty = self.get_quantities(beg_date, end_date, 'negative', product.id)
            pos_qty = self.get_quantities(beg_date, end_date, 'postive', product.id)
            adj_qty = '{:,.0f}'.format(pos_qty - neg_qty)

            prod_details.append({
                'prod_name': product.name,
                'beg_qty': beg_qty,
                'in_qty': in_qty,
                'out_qty': out_qty,
                'end_qty': end_qty,
                'adj_qty': adj_qty
            })

        report_data = {
            'beg_date': beg_date,
            'end_date': end_date,
            'lines': prod_details
        }

        return report_data

    @api.model
    def _get_report_values(self, docids, data=None):
        if data:
            return self.print_inv_report(data)
        else:
            raise UserError(_("Form content is missing, this report cannot be printed."))