# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = "sale.order"

    book_id = fields.Many2one('library.book', string='Libros')

    def action_confirm(self):
        if self.book_id:
            self.book_id.write({'state': 'borrowed'})
            return super().action_confirm()
        else:
            return super().action_confirm()




