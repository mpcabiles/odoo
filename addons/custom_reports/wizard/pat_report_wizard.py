from odoo import fields, models
from datetime import datetime, time

class PatronageReportWizard(models.TransientModel):
    _name = 'pat.report.wizard'
    options = [
        ('summary', 'Summary'),
        ('individual', 'Individual')
    ]

    start_date = fields.Datetime(required=True, default=fields.Datetime.now)
    end_date = fields.Datetime(required=True, default=fields.Datetime.now)
    #report_type = fields.Selection(selection=options, string="Type")

    def get_pat_report(self):
        date_start = fields.Datetime.to_string(datetime.combine(self.start_date.date(), time.min))
        date_stop = fields.Datetime.to_string(datetime.combine(self.end_date.date(), time.max))
        #type = report_type
        report = self.env['ir.actions.report'].search([('report_name', '=', 'custom_reports.report_pat_report')])
        data = {'date_start': date_start, 'date_stop': date_stop}
        return report.report_action(self, data=data)