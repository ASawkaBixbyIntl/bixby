# -*- coding: utf-8 -*-
{
    "name": "Bixby: CRM Lead analysis Report",
    'summary': "Web",
    'description': """
Bixby: CRM Lead analysis Report
================================
Lead analysis report with following measures
- Total number of days since created
- How many times it has moved stages
- Number of days opportunity was in each stage
- Number of opportunities in each stage
- Percentage or ration of how many opportunities made it into and out of each stage
""",
    "author": "Odoo Inc",
    'website': "https://www.odoo.com",
    'category': 'Custom Development',
    'version': '0.1',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'report/crm_lead_stats_report_views.xml',
        'report/crm_stage_activity.xml'
    ],
    'license': 'OEEL-1',
}