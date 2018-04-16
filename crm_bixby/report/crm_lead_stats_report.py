# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools


class CrmLeadStatsReport(models.Model):
    _name = "crm.lead.stats.report"
    _auto = False
    _description = "CRM Lead Statistics Analysis"
    _rec_name = 'move_count'

    lead_id = fields.Many2one(comodel_name='crm.lead', string='Lead/Opportunity', readonly=True)
    stage_id = fields.Many2one(comodel_name='crm.stage', string='Stage', readonly=True)
    user_id = fields.Many2one(comodel_name='res.users', string='Salesperson', readonly=True)
    lead_age = fields.Integer(string='Stage Update Days', readonly=True)
    move_count = fields.Integer(string='#Count Stage Changed', readonly=True)

    def _select(self):
        return """
            SELECT
                c.id,
                c.id as lead_id,
                c.user_id,
                c.stage_id,
                count(mt.id) as move_count,
                date_part('days', age(CURRENT_DATE, c.create_date::date)) as lead_age
        """

    def _from(self):
        return """
            FROM crm_lead c
        """

    def _join(self):
        return """
            JOIN mail_message AS mm on mm.res_id = c.id
            JOIN mail_tracking_value AS mt on mt.mail_message_id = mm.id and mt.field = 'stage_id'
        """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
                GROUP BY c.id, c.stage_id
            )
        """ % (self._table, self._select(), self._from(), self._join())
        )
 