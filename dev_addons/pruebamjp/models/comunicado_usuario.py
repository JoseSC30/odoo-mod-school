
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class comunicado_usuario(models.Model):
    _name = 'pruebamjp.comunicado_usuario'
    _description = 'Modelo o tabla comunicado_usuario'

    visto = fields.Boolean(string='Visto', default=False, required=True)
    comunicado_id = fields.Many2one('pruebamjp.comunicado', string="Comunicado", ondelete='cascade', required=True)
    usuario_recibe_id = fields.Many2one(
        'res.users', 
        string='Usuarios', 
        domain=lambda self: self._get_domain_usuarios(),
        required=True
    )
    tutor_usuario_info = fields.Char(
        string='Información del Tutor y Usuario', 
        compute='_compute_tutor_usuario_info'
    )


    _sql_constraints = [
        ('unique_comunicado_usuario', 'unique(comunicado_id, usuario_recibe_id)', 'El usuario ya ha recibido este comunicado.')
    ]   

    @api.model
    def _get_domain_usuarios(self):
        tutores = self.env['pruebamjp.tutor'].search([])
        usuario_ids = tutores.mapped('usuario_id.id')
        return [('id', 'in', usuario_ids)]



        




















    #@api.model
    #def _get_domain_usuarios(self):
        # Obtener todos los registros de tutores
    #    tutores = self.env['pruebamjp.tutor'].search([])

        # Extraer los IDs de usuarios relacionados con esos tutores
    #    usuario_ids = tutores.mapped('usuario_id.id')

        # Devolver el dominio que filtra usuarios por los IDs obtenidos
    #    return [('id', 'in', usuario_ids)]
    
   
    

    @api.depends('usuario_recibe_id')
    def _compute_tutor_usuario_info(self):
        for record in self:
            if record.usuario_recibe_id:
                tutor = self.env['pruebamjp.tutor'].search([('usuario_id', '=', record.usuario_recibe_id.id)], limit=1)
                if tutor:
                    curso=tutor.estudiante_tutor.estudiante.inscripcion_ids.curso                
                   # record.tutor_usuario_info = f"Tutor: {tutor.nombre} {tutor.apellido} , Usuario: {record.usuario_recibe_id.name}"
                    record.tutor_usuario_info = f"Tutor: {tutor.nombre} {tutor.apellido} , Curso: {curso.nombre} {curso.paralelo} -{curso.ciclo_id.nombre}"
                else:
                    record.tutor_usuario_info = f"Usuario: {record.usuario_recibe_id.name}"
            else:
                record.tutor_usuario_info = "No asignado"













    #usuario_envia_id = fields.Many2one('res.users', string='UsuarioEnvia', default=lambda self: self.env.user)
    #usuario_recibe_id = fields.Many2one('pruebamjp.tutor', string='UsuarioFinal',required=True)
  
    @api.model
    def default_get(self, fields_list):
        res = super(comunicado_usuario, self).default_get(fields_list)
        user = self.env.user
        if 'usuario_envia_id' in fields_list:
            res['usuario_envia_id'] = user.id
        return res


    def _create_comunicado_usuarios(self, users):
        comunicado_usuario_model = self.env['pruebamjp.comunicado_usuario']
        for user in users:
            comunicado_usuario_model.create({
                'visto': 'no',
                'comunicado_id': self.id,
                'usuario_recibe_id': user.id,
            })    


    