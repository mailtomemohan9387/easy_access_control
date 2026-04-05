from lxml import etree

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccessManager(models.Model):
    _name = 'access.manager'
    _description = 'Easy Access Control'
    _rec_name = 'name'

    name = fields.Char(string="Rule Name", required=True)
    user_id = fields.Many2one('res.users', string="User", required=True)
    model_id = fields.Many2one('ir.model', string="Model", required=True, ondelete='cascade')
    active = fields.Boolean(string="Active", default=True)
    notes = fields.Text(string="Notes")

    can_read = fields.Boolean(string="Read", default=True)
    can_create = fields.Boolean(string="Create", default=True)
    can_write = fields.Boolean(string="Write", default=True)
    can_delete = fields.Boolean(string="Delete", default=True)

    hide_create = fields.Boolean(string="Hide Create Button")
    hide_edit = fields.Boolean(string="Hide Edit Button")
    hide_delete = fields.Boolean(string="Hide Delete Button")

    _sql_constraints = [
        (
            'unique_user_model_rule',
            'unique(user_id, model_id)',
            'A rule already exists for this user and model.'
        )
    ]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_access_rule(self):
        return self.env['access.manager'].search([
            ('user_id', '=', self.env.user.id),
            ('model_id.model', '=', 'res.partner'),
            ('active', '=', True),
        ], limit=1)

    def _is_easy_access_bypassed(self):
        return self.env.is_superuser() or self.env.user.has_group('base.group_system')

    def _check_easy_access(self, operation):
        if self._is_easy_access_bypassed():
            return

        rule = self._get_access_rule()
        if not rule:
            return

        if operation == 'read' and not rule.can_read:
            raise UserError(_("You are not allowed to view Contacts."))
        elif operation == 'create' and not rule.can_create:
            raise UserError(_("You are not allowed to create Contacts."))
        elif operation == 'write' and not rule.can_write:
            raise UserError(_("You are not allowed to edit Contacts."))
        elif operation == 'unlink' and not rule.can_delete:
            raise UserError(_("You are not allowed to delete Contacts."))

    @api.model_create_multi
    def create(self, vals_list):
        self._check_easy_access('create')
        return super().create(vals_list)

    def write(self, vals):
        self._check_easy_access('write')
        return super().write(vals)

    def unlink(self):
        self._check_easy_access('unlink')
        return super().unlink()

    def read(self, fields=None, load='_classic_read'):
        self._check_easy_access('read')
        return super().read(fields=fields, load=load)

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        self._check_easy_access('read')
        return super().search_read(
            domain=domain,
            fields=fields,
            offset=offset,
            limit=limit,
            order=order
        )

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)

        if self._is_easy_access_bypassed():
            return result

        rule = self._get_access_rule()
        if not rule:
            return result

        arch = result.get('arch')
        if not arch:
            return result

        try:
            doc = etree.XML(arch)
        except Exception:
            return result

        if view_type in ('tree', 'form', 'kanban'):
            if rule.hide_create:
                for node_name in ('tree', 'form', 'kanban'):
                    for node in doc.xpath(f'//{node_name}'):
                        node.set('create', '0')

            if rule.hide_edit:
                for node_name in ('form', 'tree', 'kanban'):
                    for node in doc.xpath(f'//{node_name}'):
                        node.set('edit', '0')

            if rule.hide_delete:
                for node_name in ('form', 'tree', 'kanban'):
                    for node in doc.xpath(f'//{node_name}'):
                        node.set('delete', '0')

                for action_node in doc.xpath("//button[@name='unlink']"):
                    action_node.set('invisible', '1')

        result['arch'] = etree.tostring(doc, encoding='unicode')
        return result
