
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class gestion(models.Model):
    _name = 'pruebamjp.gestion'
    _description = 'Modelo o tabla gestion'
    year = fields.Integer(required=True,string="año")
    fecha_inicio = fields.Datetime(required=True)
    fecha_fin = fields.Datetime(required=True)
    curso_materia_ids = fields.One2many('pruebamjp.curso_materia', 'gestion_id', string="Gestiones")
    modalidad_gestion_id = fields.Many2one('pruebamjp.modalidad_gestion', string="Modalidad de Gestión", ondelete='cascade', required=True)
    inscripcion_ids = fields.One2many('pruebamjp.inscripcion', 'gestion_id', string="Gestiones")
  



    @api.depends('year','fecha_inicio','fecha_fin') 
    def _compute_display_name(self): 
         for rec in self: 
             rec.display_name = f"{rec.year}" 


    @api.constrains('year')
    def _check_unique_estudiante(self):
        for rec in self:
            existing_records = self.search([
                ('year', '=', rec.year),
                ('id', '!=', rec.id)
            ])
            if existing_records:
                raise ValidationError('ya existe la gestion')

    def unlink(self):
        for gestiones in self:
            if gestiones.curso_materia_ids or gestiones.inscripcion_ids:
                raise ValidationError("No se puede eliminar la gestion porque esta relacionada a un curso  o hay inscripciones")
        return super(gestion, self).unlink() 


    @api.constrains('year')
    def _check_year(self):
        for record in self:
            if record.year < 2000:
                raise ValidationError("El año no puede ser menor a 2000.")                                   