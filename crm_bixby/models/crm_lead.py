# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models


class CrmStageActivity(models.Model):
    _name = 'crm.stage.activity'
    _rec_name = 'lead_id'

    lead_id = fields.Many2one(comodel_name='crm.lead', string='Lead/Opportunity')
    stage_id = fields.Many2one(comodel_name='crm.stage', string='Stage')
    user_id = fields.Many2one(comodel_name='res.users', string='Salesperson')
    date_stage_changed = fields.Datetime(string='Date Stage Updated')
    date_last_stage_changed = fields.Datetime(string='Last Stage Updated')
    stage_change_age = fields.Float(compute='_compute_stage_age', store=True)

    @api.multi
    @api.depends('date_last_stage_changed')
    def _compute_stage_age(self):
        for activity in self:
            activity.stage_change_age = (fields.Datetime.from_string(fields.Datetime.now()) - fields.Datetime.from_string(activity.date_last_stage_changed)).days


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    stage_activity_ids = fields.One2many(comodel_name='crm.stage.activity', inverse_name='lead_id', string='Stage Activity History')

    @api.multi
    def write(self, vals):
        ret = super(CrmLead, self).write(vals)
        if vals.get('stage_id', False) and ret:
            self.env['crm.stage.activity'].create({
                'lead_id': self.id,
                'stage_id': self.stage_id.id,
                'user_id': self.env.user.id,
                'date_stage_changed': fields.Datetime.now(),
                'date_last_stage_changed': self.date_last_stage_update
            })
        return ret

    @api.model
    def create(self, vals):
        lead = super(CrmLead, self).create(vals)
        if lead and vals.get('stage_id', False):
            self.env['crm.stage.activity'].create({
                'lead_id': lead.id,
                'stage_id': lead.stage_id.id,
                'user_id': self.env.user.id,
                'date_stage_changed': fields.Datetime.now(),
                'date_last_stage_changed': self.date_last_stage_update
            })
        return lead
