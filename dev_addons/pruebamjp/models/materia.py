from odoo import models, fields, api
from odoo.exceptions import ValidationError

class materia(models.Model):
     _name = 'pruebamjp.materia'
     _description = 'Modelo o tabla materia'

     nombre = fields.Char(required=True)
     curso_materia_ids = fields.One2many('pruebamjp.curso_materia', 'materia_id', string="Materias del Curso")



     
     @api.depends('nombre') 
     def _compute_display_name(self): 
         for rec in self: 
             rec.display_name = f"{rec.nombre}" 



     @api.model
     def create(self, vals):
        if 'nombre' in vals:
            vals['nombre'] = vals['nombre'].upper()
        return super(materia, self).create(vals)            

     @api.constrains('nombre')
     def _mayusculas(self):
        for record in self:
            if record.nombre != record.nombre.upper():
                raise ValidationError('el campo nombre  debe estar en mayúsculas.')

     @api.constrains('nombre')
     def _check_unique_materia(self):
        for rec in self:
            existing_records = self.search([
                ('nombre', '=', rec.nombre),
                
                
                ('id', '!=', rec.id)
            ])
            if existing_records:
                raise ValidationError('ya existe la materia')
                
     def unlink(self):
        for materias in self:
            if materias.curso_materia_ids :
                raise ValidationError("No se puede eliminar materia porque esta relacionada a un curso.")
        return super(materia, self).unlink()                                        