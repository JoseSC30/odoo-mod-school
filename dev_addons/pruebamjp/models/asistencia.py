
# from odoo import models, fields, api
from odoo.exceptions import ValidationError
# from datetime import date
from odoo import models, fields, api
from datetime import date
class asistencia(models.Model):
     _name = 'pruebamjp.asistencia'
     _description = 'Modelo o tabla asistencia'
    
    
     curso_materia_id = fields.Many2one('pruebamjp.curso_materia', string="Curso Materia", required=True)
     estudiante_id = fields.Many2one('pruebamjp.estudiante', string="Estudiante")
     gestion_id = fields.Many2one('pruebamjp.gestion', string="Gestion", compute='_compute_gestion_id', store=True)
     fecha = fields.Datetime(string="Fecha", default=fields.Date.context_today, required=True)
     asistencia_line_ids = fields.One2many('pruebamjp.asistencialine', 'asistencia_id', string="Líneas de Asistencia")

     @api.depends('curso_materia_id')
     def _compute_gestion_id(self):
        for record in self:
            record.gestion_id = record.curso_materia_id.gestion_id.id if record.curso_materia_id else False

     @api.onchange('curso_materia_id')
     def load_estudiantes(self):
        for record in self:
            if record.curso_materia_id and record.gestion_id:
                estudiantes = self.env['pruebamjp.inscripcion'].search([
                    ('curso', '=', record.curso_materia_id.curso_id.id),
                    ('gestion_id', '=', record.gestion_id.id)
                ]).mapped('estudiante')
                
                record.asistencia_line_ids = [(5, 0, 0)]  # Borrar líneas existentes
                record.asistencia_line_ids = [(0, 0, {
                    'estudiante_id': estudiante.id,
                }) for estudiante in estudiantes]

     
     
     @api.constrains('curso_materia_id', 'fecha')
     def _check_duplicate_asistencia(self):
        for record in self:
            existing_asistencia = self.search([
                ('curso_materia_id', '=', record.curso_materia_id.id),
                ('fecha', '=', record.fecha),
                ('id', '!=', record.id)
            ])
            if existing_asistencia:
                raise ValidationError('Ya existe un registro de asistencia para este curso materia en la fecha especificada.')    
     
     @api.constrains('curso_materia_id')
     def _check_profesor_curso_materia(self):
        usuario_id = self.env.uid
        profesor = self.env['pruebamjp.profesor'].search([('usuario_id', '=', usuario_id)], limit=1)
        for record in self:
            if profesor and record.curso_materia_id.profesor_id != profesor:
                raise ValidationError('No puedes registrar asistencia para un curso que no está relacionado contigo.')



     @api.constrains('fecha')
     def _check_fecha_gestion(self):
        for record in self:
            if record.gestion_id:
                if record.fecha < record.gestion_id.fecha_inicio or record.fecha > record.gestion_id.fecha_fin:
                    raise ValidationError(f'La fecha de asistencia debe estar entre {record.gestion_id.fecha_inicio} y {record.gestion_id.fecha_fin}.')


 



class asistencialine(models.Model):
      _name = 'pruebamjp.asistencialine'
      _description = 'Línea de Asistencia'

      asistencia_id = fields.Many2one('pruebamjp.asistencia', string="Asistencia", required=True, ondelete='cascade')
      estudiante_id = fields.Many2one('pruebamjp.estudiante', string="Estudiante", required=True)
      asistio = fields.Boolean(string="Asistió", default=False)





#




















class asistenciawizard(models.Model):
    _name = 'pruebamjp.asistenciawizard'
    _description = 'Wizard para registrar asistencia'

    curso_materia_id = fields.Many2one('pruebamjp.curso_materia', string="Curso Materia", required=True)
    asistencia_line_ids = fields.One2many('pruebamjp.asistencia_wizard_line', 'wizard_id', string="Asistencia")

    # @api.onchange('curso_materia_id')
    # def _onchange_curso_materia_id(self):
    #     if self.curso_materia_id:
    #         inscripciones = self.env['pruebamjp.inscripcion'].search([
    #             ('curso', '=', self.curso_materia_id.curso_id.id),
    #             ('gestion_id', '=', self.curso_materia_id.gestion_id.id)
    #         ])
    #         estudiantes = inscripciones.mapped('estudiante')
    #         lines = []
    #         for estudiante in estudiantes:
    #             lines.append((0, 0, {
    #                 'estudiante': estudiante.id,
    #                 'curso_materia_id': self.curso_materia_id.id,
    #                 'fecha': fields.Date.today(),
    #             }))
    #         self.asistencia_line_ids = lines

    # def action_confirm(self):
    #     for line in self.asistencia_line_ids:
    #         self.env['pruebamjp.asistencia'].create({
    #             'curso_materia_id': line.curso_materia_id.id,
    #             'estudiante': line.estudiante.id,
    #             'gestion_id': self.curso_materia_id.gestion_id.id,
    #             'fecha': line.fecha,
    #             'asistio': line.asistio,
    #         })

class asistenciawizardline(models.TransientModel):
    _name = 'pruebamjp.asistencia_wizard_line'
    _description = 'Línea del Wizard de Asistencia'

    wizard_id = fields.Many2one('pruebamjp.asistencia_wizard', string="Wizard")
    estudiante_id = fields.Many2one('pruebamjp.estudiante', string="Estudiante", required=True)
    curso_materia_id = fields.Many2one('pruebamjp.curso_materia', string="Curso Materia", required=True)
    fecha = fields.Date(string="Fecha", default=fields.Date.context_today, required=True)
    asistio = fields.Boolean(string="Asistió", default=False, required=True)


   
    

    #@api.model
    #def create(self, vals):
        # Convertir a mayúsculas antes de crear el registro
    #    if 'nombre' in vals:
    #        vals['nombre'] = vals['nombre'].upper()
    #    if 'apellido' in vals:
    #        vals['apellido'] = vals['apellido'].upper()
    #    return super(tutor, self).create(vals) 

    
    #@api.constrains('nombre', 'apellido')
    #def _check_mayusculas(self):
    #    for record in self:
    #        # Validar que los campos estén en mayúsculas
    #        if record.nombre != record.nombre.upper() or record.apellido != record.apellido.upper():
    #            raise ValidationError('Los campos nombre y apelliido deben estar en mayúsculas.')
   
   
   
    #@api.depends('nombre', 'apellido') 
    #def _compute_display_name(self): 
    #     for rec in self: 
    #         rec.display_name = f"{rec.nombre} {rec.apellido}"

   




    #@api.constrains('nombre','apellido')
    #def _check_unique_tutor(self):
    #    for rec in self:
    #        existing_records = self.search([
    #            ('nombre', '=', rec.nombre),
    #            ('apellido', '=', rec.apellido),
                
                
    #            ('id', '!=', rec.id)
    #        ])
    #        if existing_records:
    #            raise ValidationError('ya existe el tutor')           