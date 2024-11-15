
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class subnota(models.Model):
    _name = 'pruebamjp.subnota'
    _description = 'Modelo o tabla subnota'

    nota = fields.Float(required=True)
    numero = fields.Integer(required=True,string="numero de periodo academico")
    curso_materia_id = fields.Many2one('pruebamjp.curso_materia', string="Curso_Materia", ondelete='cascade', required=True)
    curso_nombre = fields.Char(related='curso_materia_id.curso_id.nombre', string='Curso') 
    curso_paralelo = fields.Char(related='curso_materia_id.curso_id.paralelo', string='Paralelo')
    materia_nombre=fields.Char(related='curso_materia_id.materia_id.nombre', string='Materia')
    year=fields.Integer(related='curso_materia_id.gestion_id.year', string='Año')

    estudiante_id = fields.Many2one('pruebamjp.estudiante', string="Estudiante", ondelete='cascade')
    subinscripcion_id = fields.Many2one('pruebamjp.inscripcion', string="Inscripcion", ondelete='cascade',required=True)
    estudiante_nombre = fields.Char(string='Estudiante', compute='_compute_estudiante_nombre')
    notafinal = fields.Float(string='Promedio', compute='_compute_notafinal', store=True)

    


    @api.depends('curso_materia_id', 'estudiante_id', 'nota', 'year','nota')
    def _compute_notafinal(self):
        for record in self:
            subnotas = self.env['pruebamjp.subnota'].search([
                ('curso_materia_id', '=', record.curso_materia_id.id),
                ('estudiante_id', '=', record.estudiante_id.id),
                ('year', '=', record.curso_materia_id.gestion_id.year)
            ])
            total_notas = sum(subnota.nota for subnota in subnotas)
            record.notafinal = total_notas / len(subnotas) if subnotas else record.nota



    @api.constrains('curso_materia_id', 'inscripcion_id')
    def _check_year(self):
        for record in self:
            if record.curso_materia_id.gestion_id.year != record.subinscripcion_id.gestion_id.year:
                raise ValidationError("El año de la gestión del curso materia y la inscripción deben coincidir.")  
     





    # @api.constrains('curso_materia_id', 'estudiante_id', 'numero', 'year')
    # def _check_unique_subnota(self):
    #     for record in self:
    #         existing_subnota = self.env['pruebamjp.subnota'].search([
    #             ('curso_materia_id', '=', record.curso_materia_id.id),
    #             ('estudiante_id', '=', record.estudiante_id.id),
    #             ('numero', '=', record.numero),
    #             ('year', '=', record.year),
    #             ('id', '!=', record.id)
    #         ])
    #         if existing_subnota:
    #             raise ValidationError("Ya existe una subnota con el mismo curso, estudiante, número y año.") 




    @api.depends('subinscripcion_id')
    def _compute_estudiante_nombre(self):
        for record in self:
            if record.subinscripcion_id:
                nombre = record.subinscripcion_id.estudiante.nombre
                apellido = record.subinscripcion_id.estudiante.apellido  # Asegúrate de que 'apellido' es un campo en el modelo estudiante
                record.estudiante_nombre = f"{nombre} {apellido}"            


    @api.constrains('nota','numero')
    def _check_year(self):
        for record in self:
            if record.nota < 0 :
                raise ValidationError("la nota no puede  ser menor de 0.")
            if record.numero < 1 :
                raise ValidationError("el numero de periodo academico no puede  ser menor a 1.")                 