
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class tutor(models.Model):
    _name = 'pruebamjp.tutor'
    _description = 'Modelo o tabla tutor'

   
    nombre = fields.Char(required=True)
    apellido = fields.Char(required=True)
    telefono = fields.Char(required=True)
    direccion = fields.Char(required=True)
    estudiante_tutor=fields.One2many(string="estudiante_tutor", comodel_name="pruebamjp.estudiante_tutor",inverse_name='tutor')
    usuario_id = fields.Many2one('res.users', string='Usuario',required=True)

    @api.model
    def create(self, vals):
        if 'nombre' in vals:
            vals['nombre'] = vals['nombre'].upper()
        if 'apellido' in vals:
            vals['apellido'] = vals['apellido'].upper()
        return super(tutor, self).create(vals) 

    
    @api.constrains('nombre', 'apellido')
    def _check_mayusculas(self):
        for record in self:
            if record.nombre != record.nombre.upper() or record.apellido != record.apellido.upper():
                raise ValidationError('Los campos nombre y apelliido deben estar en mayúsculas.')
   
   
   
    @api.depends('nombre', 'apellido') 
    def _compute_display_name(self): 
         for rec in self: 
             rec.display_name = f"{rec.nombre} {rec.apellido}"


    @api.constrains('nombre', 'apellido', 'usuario_id')
    def _check_unique_tutor(self):
        for rec in self:
            existing_records = self.search([
                '|',
                '&',
                ('nombre', '=', rec.nombre),
                ('apellido', '=', rec.apellido),
                ('usuario_id', '=', rec.usuario_id.id),
                ('id', '!=', rec.id)
            ])
            if existing_records:
                raise ValidationError('Ya existe un tutor con el mismo nombre y apellido, o ya hay un tutor asignado al usuario.')           