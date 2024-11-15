
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class comunicado(models.Model):
    _name = 'pruebamjp.comunicado'
    _description = 'Modelo o tabla comunicado'

    nombre = fields.Char(required=True)
    description = fields.Text(required=True)
    fecha = fields.Datetime(required=True)
    comunicado_usuario_ids = fields.One2many('pruebamjp.comunicado_usuario', 'comunicado_id', string="Comunicados")
    curso_id = fields.Many2one('pruebamjp.curso', string="Curso")
    
    
    def create_comunicado_for_all_users(self):
        users = self.env['res.users'].search([])
        self._create_comunicado_usuarios(users)



    def _create_comunicado_usuarios(self, users):
        comunicado_usuario_model = self.env['pruebamjp.comunicado_usuario']
        for user in users:
            comunicado_usuario_model.create({
                'visto': 'no',
                'comunicado_id': self.id,
                'usuario_recibe_id': user.id,
            })

     
    def create_comunicado_for_tutors_of_course(self):
        if not self.curso_id:
            raise ValidationError("Por favor, seleccione un curso.")
        max_year = self.env['pruebamjp.gestion'].search([], order='year desc', limit=1).year
        inscripciones = self.env['pruebamjp.inscripcion'].search([
        ('curso', '=', self.curso_id.id),
        ('gestion_id.year', '=', max_year)
        ])
        estudiante_ids = inscripciones.mapped('estudiante.id')
        estudiante_tutores = self.env['pruebamjp.estudiante_tutor'].search([('estudiante', 'in', estudiante_ids)])
        tutor_ids = estudiante_tutores.mapped('tutor.id')
        usuarios = self.env['res.users'].search([('id', 'in', self.env['pruebamjp.tutor'].browse(tutor_ids).mapped('usuario_id.id'))])
        self._create_comunicado_usuarios(usuarios)

    @api.model
    def create(self, vals):
        record = super(comunicado, self).create(vals)
        return record    
 

    @api.depends('nombre') 
    def _compute_display_name(self): 
         for rec in self: 
             rec.display_name = f"{rec.nombre}" 
 
       
