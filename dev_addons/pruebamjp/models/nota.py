
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class nota(models.Model):
    _name = 'pruebamjp.nota'
    _description = 'Modelo o tabla nota'

    nota = fields.Float(required=True)
    
    
    curso_materia_id = fields.Many2one('pruebamjp.curso_materia', string="Curso_Materia", ondelete='cascade', required=True)
    curso_nombre = fields.Char(related='curso_materia_id.curso_id.nombre', string='Curso') 
    curso_paralelo = fields.Char(related='curso_materia_id.curso_id.paralelo', string='Paralelo')
    materia_nombre=fields.Char(related='curso_materia_id.materia_id.nombre', string='Materia')
    year=fields.Integer(related='curso_materia_id.gestion_id.year', string='Año')
 
    estudiante_id = fields.Many2one('pruebamjp.estudiante', string="Estudiante", ondelete='cascade')
    noinscripcion_id = fields.Many2one('pruebamjp.inscripcion', string="Inscripcion", ondelete='cascade')
      

    @api.constrains('curso_materia_id', 'inscripcion_id')
    def _check_year(self):
        for record in self:
            if record.curso_materia_id.gestion_id.year != record.noinscripcion_id.gestion_id.year:
                raise ValidationError("El año de la gestión del curso materia y la inscripción deben coincidir.")  
    
    
    
    estudiante_nombre=fields.Char(related='estudiante_id.nombre', string='Estudiante')