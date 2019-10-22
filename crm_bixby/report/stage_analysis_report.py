# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, tools


class CrmStageAnalysisReport(models.Model):
    _name = "crm.stage.report"
    _auto = False
    _description = "CRM Stage Analysis"
    _rec_name = 'lead_count'

    lead_count = fields.Integer('No of Leads', readonly=True)
    stage_id = fields.Many2one('crm.stage', readonly=True)
    lead_in_count = fields.Integer('Incoming Leads', readonly=True)
    lead_out_count = fields.Integer('Outgoing Leads', readonly=True)
    perc = fields.Float('In/Out Percent', readonly=True)

    def _select(self):
        return """
            SELECT
                s.id,
                s.id as stage_id,
                s.name,
                (SELECT count(l.id) from crm_lead l where l.stage_id = s.id) as lead_count,
                (SELECT count(DISTINCT m.res_id) from mail_tracking_value t JOIN mail_message m on m.res_id in (SELECT id from crm_lead where stage_id = s.id) and m.model = 'crm.lead' and t.field = 'stage_id' and t.mail_message_id = m.id and t.new_value_integer = s.id) as lead_in_count,
                (SELECT count(DISTINCT m.res_id) from mail_tracking_value t JOIN mail_message m on m.res_id in (SELECT id from crm_lead) and m.model = 'crm.lead' and t.field = 'stage_id' and t.mail_message_id = m.id and t.old_value_integer = s.id) as lead_out_count,
                (SELECT count(DISTINCT m.res_id) from mail_tracking_value t JOIN mail_message m on m.res_id in (SELECT id from crm_lead) and m.model = 'crm.lead' and t.field = 'stage_id' and t.mail_message_id = m.id and t.old_value_integer = s.id) * 100 / (SELECT count(DISTINCT m.res_id) from mail_tracking_value t JOIN mail_message m on m.res_id in (SELECT id from crm_lead where stage_id = s.id) and m.model = 'crm.lead' and t.field = 'stage_id' and t.mail_message_id = m.id and t.new_value_integer = s.id) as perc
        """

    def _from(self):
        return """
            FROM crm_stage s
        """

    def _join(self):
        return """
            JOIN crm_lead AS l on l.stage_id = s.lead_id
        """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
            )
        """ % (self._table, self._select(), self._from())
        )
