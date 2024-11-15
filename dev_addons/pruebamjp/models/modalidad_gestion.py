
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class modalidad_gestion(models.Model):
    _name = 'pruebamjp.modalidad_gestion'
    _description = 'Modelo o tabla modalidad gestion'

    nombre = fields.Char(required=True)
    gestion = fields.One2many('pruebamjp.gestion', 'modalidad_gestion_id', string="gestiones")
    
    @api.depends('nombre') 
    def _compute_display_name(self): 
         for rec in self: 
             rec.display_name = f"{rec.nombre} "

    @api.model
    def create(self, vals):
        if 'nombre' in vals:
            vals['nombre'] = vals['nombre'].upper()
        return super(modalidad_gestion, self).create(vals) 
    
    @api.constrains('nombre')
    def _check_mayusculas(self):
        for record in self:
            if record.nombre != record.nombre.upper() :
                raise ValidationError('Los campos nombre deben estar en mayúsculas.')


    def unlink(self):
        for modalidades in self:
            if  modalidades.gestion :
                raise ValidationError("No se puede eliminar la modalidad porque tiene  gestiones asociadas.")
        return super(estudiante, self).unlink()                  