
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class horario(models.Model):
    _name = 'pruebamjp.horario'
    _description = 'Modelo o tabla horario'

    hora_inicio = fields.Integer(required=True)
    minuto_inicio=fields.Integer(required=True)
    hora_fin = fields.Integer(required=True)
    minuto_fin=fields.Integer(required=True)
    dia = fields.Selection([
        ('LUNES', 'LUNES'),
        ('MARTES', 'MARTES'),
        ('MIERCOLES', 'MIERCOLES'),
        ('JUEVES', 'JUEVES'),
        ('VIERNES', 'VIERNES'),
        ('SABADO', 'SABADO')])

    
    curso_materia_ids = fields.One2many('pruebamjp.curso_materia', 'horario_id', string="Horarios")
     
    

    



    @api.model
    def create(self, vals):
        if 'dia' in vals:
            vals['dia'] = vals['dia'].upper()
        return super(horario, self).create(vals)

   

    @api.constrains('hora_inicio', 'minuto_inicio', 'hora_fin', 'minuto_fin')
    def _check_time_intervals(self):
        for record in self:
            inicio_total_minutos = record.hora_inicio * 60 + record.minuto_inicio
            fin_total_minutos = record.hora_fin * 60 + record.minuto_fin
            diferencia = fin_total_minutos - inicio_total_minutos
            if diferencia % 45 != 0:
                raise ValidationError("La diferencia entre la hora de inicio y la hora de fin debe ser múltiplo de 45 minutos.")
            if not (0 <= record.hora_inicio < 24 and 0 <= record.minuto_inicio < 60 and 
                    0 <= record.hora_fin < 24 and 0 <= record.minuto_fin < 60):
                raise ValidationError("Las horas y minutos deben estar en un rango válido.")
            if inicio_total_minutos >= fin_total_minutos:
                raise ValidationError("La hora de inicio debe ser anterior a la hora de fin.")



    @api.constrains('hora_inicio', 'hora_fin','minuto_inicio','minuto_fin')
    def _check_horas(self):
        for record in self:
            if record.hora_inicio < 7 or record.hora_inicio > 23:
                raise ValidationError("La hora de inicio debe estar entre 7:00 y 23:00.")

            if record.hora_fin < record.hora_inicio:
                raise ValidationError("La hora final no puede ser menor que la hora de inicio.")

            if record.hora_fin > 23:
                raise ValidationError("La hora final no puede ser mayor que las 23:00.")

            if record.minuto_inicio < 0 or record.minuto_inicio > 59 :
                raise ValidationError("los minutos no pueden ser mayor a 59 o menores a 0")    
            
            if record.minuto_fin < 0 or record.minuto_fin > 59:
                raise ValidationError("los minutos no pueden ser mayor a 59 o menores a 0") 


    @api.depends('hora_inicio','hora_fin') 
    def _compute_display_name(self): 
         for rec in self: 
             rec.display_name = f"horario {rec.hora_inicio}:{rec.minuto_inicio} - {rec.hora_fin}:{rec.minuto_fin} - {rec.dia}"

   
    @api.constrains('hora_inicio','hora_fin','minuto_inicio','minuto_fin','dia')
    def _check_unique_estudiante(self):
        for rec in self:
            existing_records = self.search([
                ('hora_inicio', '=', rec.hora_inicio),
                ('hora_fin', '=', rec.hora_fin),
                ('minuto_inicio', '=', rec.minuto_inicio),
                ('minuto_fin', '=', rec.minuto_fin),
                ('dia', '=', rec.dia),
                
                
                ('id', '!=', rec.id)
            ])
            if existing_records:
                raise ValidationError('ya existe el horario')



 
    def unlink(self):
        for horarios in self:
            if horarios.curso_materia_ids :
                raise ValidationError("No se puede eliminar el horario porque esta relacionada a un curso.")
        return super(horario, self).unlink()                             