from odoo import api, models
from odoo.exceptions import UserError
from datetime import datetime

class InvReport(models.AbstractModel):
    _name = 'report.custom_reports.report_pat_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data:
            return self.print_pat_report(data)
        else:
            raise UserError(_("Form content is missing, this report cannot be printed."))

    def print_pat_report(self, data):
        beg_date = datetime.strptime(data.get('date_start'), '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(data.get('date_stop'), '%Y-%m-%d %H:%M:%S')
        customers = self.env['res.partner'].search([])
        results =[]

        for customer in customers:
            orders = self.env['pos.order'].search([
                ('date_order', '>=', beg_date),
                ('date_order', '<=', end_date),
                ('partner_id', '=', customer.id)
            ])
            total = sum(orders.mapped('amount_total'))

            results.append({
                'name': customer.name,
                'total': total
            })

        return_data = {'details': results}

        return return_data