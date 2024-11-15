
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class curso_materia(models.Model):
    _name = 'pruebamjp.curso_materia'
    _description = 'Modelo o tabla curso materia'
    curso_id = fields.Many2one('pruebamjp.curso', string="Curso", ondelete='cascade', required=True)
    materia_id = fields.Many2one('pruebamjp.materia', string="Materia", ondelete='cascade', required=True)
    profesor_id = fields.Many2one('pruebamjp.profesor', string="Profesor", ondelete='cascade', required=True)
    horario_id = fields.Many2one('pruebamjp.horario', string="Horario", ondelete='cascade', required=True)
    nota_ids = fields.One2many('pruebamjp.nota', 'curso_materia_id', string="Cursos_Materias_nota")
    
    
    subnota_ids = fields.One2many('pruebamjp.subnota', 'curso_materia_id', string="Cursos_Materias_subnota")
    gestion_id = fields.Many2one('pruebamjp.gestion', string="Gestion", ondelete='cascade', required=True) 
    
    @api.constrains('horario_id')
    def _check_horario_conflict(self):
        for record in self:
            existing_records = self.env['pruebamjp.curso_materia'].search([
                ('curso_id', '=', record.curso_id.id),
                ('horario_id.dia', '=', record.horario_id.dia),
                ('id', '!=', record.id)
            ])

            for existing in existing_records:
                if self._is_overlap(existing.horario_id, record.horario_id):
                    raise ValidationError("Conflicto de horario detectado para el curso {} y materia {} en el día {}.".format(
                        record.curso_id.nombre, record.materia_id.nombre, record.horario_id.dia
                    ))

    def _is_overlap(self, horario1, horario2):
        start1 = horario1.hora_inicio * 60 + horario1.minuto_inicio
        end1 = horario1.hora_fin * 60 + horario1.minuto_fin
        start2 = horario2.hora_inicio * 60 + horario2.minuto_inicio
        end2 = horario2.hora_fin * 60 + horario2.minuto_fin
        return max(start1, start2) < min(end1, end2) 
    
    @api.depends('curso_id','gestion_id') 
    def _compute_display_name(self): 
         for rec in self: 
             rec.display_name = f"{rec.curso_id.nombre} {rec.curso_id.paralelo}- {rec.materia_id.nombre} -{rec.gestion_id.year}" 


    @api.constrains('curso_id', 'materia_id')
    def _check_unique_curso_materia(self):
        for rec in self:
            existing_records = self.search([
                ('curso_id', '=', rec.curso_id.id),
                ('materia_id', '=', rec.materia_id.id),
                
                ('id', '!=', rec.id)
            ])
            if existing_records:
                raise ValidationError('La combinación de Curso, Materia ya existe.')    

    @api.constrains('curso_id', 'materia_id', 'horario_id')
    def _check_unique_curso_materia_horario(self):
        for rec in self:
            existing_records = self.search([
                ('curso_id', '=', rec.curso_id.id),
                ('materia_id', '=', rec.materia_id.id),
                ('horario_id', '=', rec.horario_id.id),
                ('id', '!=', rec.id)
            ])
            if existing_records:
                raise ValidationError('La combinación de Curso, Materia y Horario ya existe.')         


    @api.constrains('curso_id', 'horario_id')
    def _check_unique_course_schedule(self):
        for record in self:
            overlapping_courses = self.search([
                ('curso_id', '=', record.curso_id.id),
                ('horario_id', '=', record.horario_id.id),
                ('id', '!=', record.id)
            ])
            if overlapping_courses:
                raise ValidationError(f'El curso {record.curso_id.nombre} ya tiene una materia asignada en el horario {record.horario_id.hora_inicio}:{record.horario_id.minuto_inicio}.')
   

          


