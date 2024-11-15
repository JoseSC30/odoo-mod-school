
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class profesor(models.Model):
    _name = 'pruebamjp.profesor'
    _description = 'Modelo o tabla profesor'

    nombre = fields.Char(required=True)
    curso_materia_ids = fields.One2many('pruebamjp.curso_materia', 'profesor_id', string="Profesores")
    usuario_id = fields.Many2one('res.users', string='Usuario',required=True)

   
    @api.model
    def create(self, vals):
        if 'nombre' in vals:
            vals['nombre'] = vals['nombre'].upper()
        return super(profesor, self).create(vals)
   

    
    @api.constrains('nombre')
    def _check_mayusculas(self):
        for record in self:
            if record.nombre != record.nombre.upper() :
                raise ValidationError('Los campos nombre  debe estar en mayúsculas.')


        
    @api.depends('nombre') 
    def _compute_display_name(self): 
         for rec in self: 
             rec.display_name = f"{rec.nombre}" 


    @api.constrains('nombre', 'usuario_id')
    def _check_unique_profesor(self):
        for rec in self:
            existing_records = self.search([
                '|',
                ('nombre', '=', rec.nombre),
                ('usuario_id', '=', rec.usuario_id.id),
                ('id', '!=', rec.id)
            ])
            if existing_records:
                raise ValidationError('Ya existe un profesor con el mismo nombre o ya hay un profesor asignado al usuario.')
    
    
    def unlink(self):
        for profesores in self:
            if profesores.curso_materia_ids :
                raise ValidationError("No se puede eliminar el profesor porque esta relacionado a un curso.")
        return super(profesor, self).unlink()                            