
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ciclo(models.Model):
    _name = 'pruebamjp.ciclo'
    _description = 'Modelo o tabla ciclo'

    nombre = fields.Char(required=True)
    curso_id = fields.One2many('pruebamjp.curso', 'ciclo_id', string="Ciclos")


    @api.depends('nombre') 
    def _compute_display_name(self): 
         for rec in self: 
             rec.display_name = f"{rec.nombre}" 




    @api.constrains('nombre')
    def _check_unique_curso_materia(self):
        for rec in self:
            existing_records = self.search([
                ('nombre', '=', rec.nombre),
                
                ('id', '!=', rec.id)
            ])
            if existing_records:
                raise ValidationError('ya existe el ciclo')          


    @api.model
    def create(self, vals):
        if 'nombre' in vals:
            vals['nombre'] = vals['nombre'].upper()
        return super(ciclo, self).create(vals)            

    @api.constrains('nombre')
    def _mayusculas(self):
        for record in self:
            if record.nombre != record.nombre.upper():
                raise ValidationError('el campo nombre  debe estar en mayúsculas.')


    @api.constrains('nombre')
    def _check_unique_ciclo(self):
        for rec in self:
            existing_records = self.search([
                ('nombre', '=', rec.nombre),
                
                
                ('id', '!=', rec.id)
            ])
            if existing_records:
                raise ValidationError('ya existe el ciclo')
    def unlink(self):
        for ciclos in self:
            if ciclos.cursoid :
                raise ValidationError("No se puede eliminar el ciclo porque esta relacionada a un curso.")
        return super(ciclo, self).unlink()                                          