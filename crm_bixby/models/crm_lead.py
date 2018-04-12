# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models


class CrmStageActivity(models.Model):
    _name = 'crm.stage.activity'

    lead_id = fields.Many2one('crm.lead')
    stage_id = fields.Many2one('crm.stage')
    stage_age = fields.Float(compute='_compute_stage_age', store=True)
    last_stage_change_date = fields.Datetime('Last Stage Updated')

    @api.multi
    @api.depends('last_stage_change_date')
    def _compute_stage_age(self):
        for activity in self:
            activity.stage_age = (datetime.now() - fields.Datetime.from_string(activity.last_stage_change_date)).days


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.multi
    def write(self, vals):
        if vals.get('stage_id', False):
            self.env['crm.stage.activity'].create({
                'lead_id': self.id,
                'stage_id': self.stage_id.id,
                'last_stage_change_date': self.date_last_stage_update
                })
        return super(CrmLead, self).write(vals)

    @api.model
    def create(self, vals):
        lead = super(CrmLead, self).create(vals)
        if vals.get('stage_id', False):
            self.env['crm.stage.activity'].create({
                'lead_id': lead.id,
                'stage_id': lead.stage_id.id,
                'last_stage_change_date': self.date_last_stage_update
                })
        return lead
