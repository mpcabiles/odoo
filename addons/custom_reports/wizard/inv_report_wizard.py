from odoo import api, fields, models
from datetime import datetime, time, timedelta

class InvReportWizard(models.TransientModel):
    _name = 'inv.report.wizard'

    inv_start_date = fields.Datetime(required=True, default=fields.Datetime.now)
    inv_end_date = fields.Datetime(required=True, default=fields.Datetime.now)

    def get_inv_report(self):
        date_start = fields.Datetime.to_string(datetime.combine(self.inv_start_date.date(), time.min))
        date_stop = fields.Datetime.to_string(datetime.combine(self.inv_end_date.date(), time.max))
        report = self.env['ir.actions.report'].search([('report_name', '=', 'custom_reports.report_inv_report')])
        data = {'date_start': date_start, 'date_stop': date_stop}
        return report.report_action(self, data=data)