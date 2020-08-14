# -*- coding: utf-8 -*-
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class ReportSession(models.AbstractModel):
    _name = "report.openacademy.report_session_view"

    def _get_report_values(self, docids, data=None):
        # report_obj = self.env["report"]
        # report = report_obj._get_report_from_name("openacademy.report_session")
        # docargs = {
        #     "doc_ids": docids,
        #     "doc_model": report.model,
        #     "docs": self.env['openacademy.session'].browse(docids),
        #     "other_variable": 'other value',
        # }
        # return report_obj.render("openacademy.report_session_view", docargs)
        docs = self.env['openacademy.session'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'openacademy.session',
            'docs': docs,
            'other_variable': 'other value',
        }
