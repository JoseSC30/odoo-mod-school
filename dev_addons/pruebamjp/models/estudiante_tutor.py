
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class estudiante_tutor(models.Model):
    _name = 'pruebamjp.estudiante_tutor'
    _description = 'Modelo o tabla estudiante tutor'


    relacion=fields.Char() 
    estudiante = fields.Many2one("pruebamjp.estudiante",ondelete="cascade",help="estudiante relacionado",required=True)
    tutor = fields.Many2one("pruebamjp.tutor", ondelete="cascade", help="Tutor relacionado", required=True)
    estudiante_nombre = fields.Char(related='estudiante.nombre', string='Nombre del Estudiante')
    tutor_nombre = fields.Char(related='tutor.nombre', string='Nombre del tutor')
   
    @api.constrains('estudiante','tutor')
    def _check_unique_estudiante_tutor(self):
        for rec in self:
            existing_records = self.search([
                ('estudiante', '=', rec.estudiante.id),
                ('tutor', '=', rec.tutor.id),
                
                
                ('id', '!=', rec.id)
            ])
        if existing_records:
            raise ValidationError('ya existe esta combinacion de estudiante con tutor')

           