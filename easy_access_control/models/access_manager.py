from odoo import models, fields, api
from odoo.exceptions import UserError


class AccessManager(models.Model):
    _name = 'access.manager'
    _description = 'Easy Access Control'

    name = fields.Char(string="Rule Name", required=True)
    user_id = fields.Many2one('res.users', string="User", required=True)
    model_id = fields.Many2one('ir.model', string="Model", required=True, ondelete='cascade')

    can_read = fields.Boolean(string="Read")
    can_create = fields.Boolean(string="Create")
    can_write = fields.Boolean(string="Write")
    can_delete = fields.Boolean(string="Delete")

    hide_create = fields.Boolean(string="Hide Create Button")
    hide_edit = fields.Boolean(string="Hide Edit Button")
    hide_delete = fields.Boolean(string="Hide Delete Button")


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, vals_list):
        rules = self.env['access.manager'].search([
            ('user_id', '=', self.env.user.id),
            ('model_id.model', '=', 'res.partner')
        ])

        for rule in rules:
            if not rule.can_create:
                raise UserError("You are not allowed to create records!")

        return super().create(vals_list)

    def write(self, vals):
        rules = self.env['access.manager'].search([
            ('user_id', '=', self.env.user.id),
            ('model_id.model', '=', 'res.partner')
        ])

        for rule in rules:
            if not rule.can_write:
                raise UserError("You are not allowed to edit this record!")

        return super().write(vals)

    def unlink(self):
        rules = self.env['access.manager'].search([
            ('user_id', '=', self.env.user.id),
            ('model_id.model', '=', 'res.partner')
        ])

        for rule in rules:
            if not rule.can_delete:
                raise UserError("You are not allowed to delete this record!")

        return super().unlink()
