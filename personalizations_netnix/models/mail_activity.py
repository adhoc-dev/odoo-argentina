from odoo import models, fields, api

class MailActivity(models.Model):

    _inherit = 'mail.activity'

    def write(self, vals):
        old_date_deadline = self.date_deadline
        res = super().write(vals)
        if 'date_deadline' in vals:
            msj = "Se ha cambiado la fecha de fin de actividad de %s a %s" % (old_date_deadline.strftime("%d-%m-%Y"), self.date_deadline.strftime("%d-%m-%Y"))
            self.env[self.res_model].browse(self.res_id).message_post(body=msj)
        return res

    def unlink(self):
        if self:
            msj = "Se ha eliminado la actividad del tipo %s con asunto %s" % (self.activity_type_id.name, self.summary)
            self.env[self.res_model].browse(self.res_id).message_post(body=msj)
        result = super().unlink()
        return result
