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


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    def _is_easy_access_bypassed(self):
        return self.env.is_superuser() or self.env.user.has_group('base.group_system')

    def _is_easy_access_internal_model(self):
        internal_prefixes = (
            'ir.',
            'base.',
            'bus.',
            'web.',
            'mail.',
        )
        internal_models = {
            'access.manager',
            'res.users',
            'res.users.log',
            'res.groups',
            'res.company',
            'res.lang',
        }
        return self._name.startswith(internal_prefixes) or self._name in internal_models

    def _get_access_rule(self):
        if self._is_easy_access_bypassed() or self._is_easy_access_internal_model():
            return False

        # login / registry load time safe guard
        if 'access.manager' not in self.env:
            return False

        return self.env['access.manager'].sudo().search([
            ('user_id', '=', self.env.user.id),
            ('model_id.model', '=', self._name),
            ('active', '=', True),
        ], limit=1)

    def _check_easy_access(self, operation):
        if self._is_easy_access_bypassed() or self._is_easy_access_internal_model():
            return

        rule = self._get_access_rule()
        if not rule:
            return

        model_label = self._name
        ir_model = self.env['ir.model']._get(self._name)
        if ir_model and ir_model.name:
            model_label = ir_model.name

        if operation == 'read' and not rule.can_read:
            raise UserError(_("You are not allowed to view %s.") % model_label)
        elif operation == 'create' and not rule.can_create:
            raise UserError(_("You are not allowed to create %s.") % model_label)
        elif operation == 'write' and not rule.can_write:
            raise UserError(_("You are not allowed to edit %s.") % model_label)
        elif operation == 'unlink' and not rule.can_delete:
            raise UserError(_("You are not allowed to delete %s.") % model_label)

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
            order=order,
        )

    @api.model
    def get_views(self, views, options=None):
        result = super().get_views(views, options=options)

        if self._is_easy_access_bypassed() or self._is_easy_access_internal_model():
            return result

        rule = self._get_access_rule()
        if not rule:
            return result

        result_views = result.get('views', {})
        if not result_views:
            return result

        for _view_type, view_data in result_views.items():
            arch = view_data.get('arch')
            if not arch:
                continue

            try:
                doc = etree.XML(arch)
            except Exception:
                continue

            if rule.hide_create:
                for node in doc.xpath('//list | //form | //kanban'):
                    node.set('create', '0')

            if rule.hide_edit:
                for node in doc.xpath('//list | //form | //kanban'):
                    node.set('edit', '0')

            if rule.hide_delete:
                for node in doc.xpath('//list | //form | //kanban'):
                    node.set('delete', '0')

                for btn in doc.xpath("//button[@name='unlink']"):
                    btn.set('invisible', '1')

            view_data['arch'] = etree.tostring(doc, encoding='unicode')

        return result
