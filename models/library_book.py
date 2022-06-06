# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, UserError
import logging

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

logger = logging.getLogger(__name__)


class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Library Book'

    day_to_end = fields.Char('Remaining days', compute='compute_day_end', store=True)
    name = fields.Char('Title', required=True, tracking=True)
    date_release = fields.Date('Release Date', tracking=True)
    author_ids = fields.Char(string='Authors', tracking=True)
    client_id = fields.Many2one('res.partner', string='Clients', tracking=True)
    category_id = fields.Many2one('library.book.category', string='Category', tracking=True)
    book_image = fields.Binary('Image', tracking=True)
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    sale_order_id = fields.Many2one('sale.order', 'Sales Order', help="Sales order to which the task is linked.")

    state = fields.Selection([
        ('draft', 'Unavailable'),
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost')],
        'State', default="draft")

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'borrowed'),
                   ('borrowed', 'available'),
                   ('available', 'lost'),
                   ('borrowed', 'lost'),
                   ('lost', 'available')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                message = _('Moving from %s to %s is not allowd') % (book.state, new_state)
                raise UserError(message)

    def make_available(self):
        self.change_state('available')

    def make_borrowed(self):
        self.change_state('borrowed')

    def create_order(self):
        self.create_sale_order()

    def make_lost(self):
        self.change_state('lost')

    def log_all_library_members(self):
        library_member_model = self.env['library.member']  
        all_members = library_member_model.search([])
        print("ALL MEMBERS:", all_members)
        return True

    def create_categories(self):
        categ1 = {
            'name': 'Child category 1',
            'description': 'Description for child 1'
        }
        categ2 = {
            'name': 'Child category 2',
            'description': 'Description for child 2'
        }
        parent_category_val = {
            'name': 'Parent category',
            'description': 'Description for parent category',
            'child_ids': [
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }
        
        record = self.env['library.book.category'].create(parent_category_val)
        return True

    def change_release_date(self):
        self.ensure_one()
        self.date_release = fields.Date.today()

    @api.depends('date_release', 'day_to_end')
    def compute_day_end(self):
        for x in self:
            fec = fields.Date.today()
            if not x.date_release and fec:
                return
            elif x.date_release > fec:
                x.write({'date_release': fec})
                raise ValidationError(_("You are entering a date after the current one"))
            else:
                date_end = x.date_release + timedelta(days=30)
                fecha_vencimiento = date_end - fields.Date.today()
                if fecha_vencimiento.days >= 0:
                    x.day_to_end = str(fecha_vencimiento.days)
                else:
                    x.write({'state': 'lost'})
                    x.day_to_end = 'lost'

    def find_book(self):
        domain = [
            '|',
            '&', ('name', 'ilike', 'Book Name'),
            ('category_id.name', '=', 'Category Name'),
            '&', ('name', 'ilike', 'Book Name 2'),
            ('category_id.name', '=', 'Category Name 2')
        ]
        books = self.search(domain)
        logger.info('Books found: %s', books)
        return True

    # Filter recordset
    def filter_books(self):
        all_books = self.search([])
        filtered_books = self.books_with_multiple_authors(all_books)
        logger.info('Filtered Books: %s', filtered_books)

    @api.model
    def books_with_multiple_authors(self, all_books):
        def predicate(book):
            if len(book.author_ids) > 1:
                return True

        return all_books.filtered(predicate)

    # Traversing recordset
    def mapped_books(self):
        all_books = self.search([])
        books_authors = self.get_author_names(all_books)
        logger.info('Books Authors: %s', books_authors)

    @api.model
    def get_author_names(self, all_books):
        return all_books.mapped('author_ids.name')

    # Sorting recordset
    def sort_books(self):
        all_books = self.search([])
        books_sorted = self.sort_books_by_date(all_books)
        logger.info('Books before sorting: %s', all_books)
        logger.info('Books after sorting: %s', books_sorted)

    @api.model
    def sort_books_by_date(self, all_books):
        return all_books.sorted(key='date_release')

    def create_sale_order(self):
        
        product_library_book = self.env['product.product'].create({
            'name': self.name,
            'type': 'service',
        })

        order = self.env['sale.order'].create({
            'partner_id': self.client_id.id,
            'book_id': self.id,
            'order_line': [(0, 0, {
                'product_id': product_library_book.id,
                'product_uom_qty': 1,
                'price_unit': self.price_unit,
            })]
        })
        self.sale_order_id = order.id


    def _get_action_view_so_ids(self):
        return self.sale_order_id.ids

    def action_view_so(self):
        self.ensure_one()
        so_ids = self._get_action_view_so_ids()
        action_window = {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "name": "Sales Order",
            "views": [[False, "tree"], [False, "form"]],
            "context": {"create": False, "show_sale": True},
            "domain": [["id", "in", so_ids]],
        }
        if len(so_ids) == 1:
            action_window["views"] = [[False, "form"]]
            action_window["res_id"] = so_ids[0]

        return action_window


class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = "Library member"

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')
