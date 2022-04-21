# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    whatsapp_number = fields.Char("WhatsApp Number", help="Enter the Company WhatsApp Number")
