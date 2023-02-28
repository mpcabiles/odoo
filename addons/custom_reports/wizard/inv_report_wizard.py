from odoo import api, fields, models, _

class InvReportWizard(models.TransientModel):
    _name = 'inv.report.wizard'
    _description = 'Inventory Report'

    inv_start_date = fields.Datetime(required=True, default=fields.Datetime.now)
    inv_end_date = fields.Datetime(required=True, default=fields.Datetime.now)

    @api.onchange('inv_start_date')
    def _onchange_start_date(self):
        if self.inv_start_date and self.inv_end_date and self.inv_end_date < self.inv_start_date:
            self.inv_end_date = self.inv_start_date

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.inv_end_date and self.inv_end_date < self.inv_start_date:
            self.inv_start_date = self.inv_end_date