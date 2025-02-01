
from odoo import models, fields, api
from odoo.exceptions import ValidationError

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import requests
import os


class Comunicado(models.Model):
    _name = 'pruebamjp.comunicado'
    _description = 'Modelo o tabla comunicado'

    nombre = fields.Char(required=True)
    description = fields.Text(required=True)
    fecha = fields.Datetime(required=True)
    comunicado_usuario_ids = fields.One2many('pruebamjp.comunicado_usuario', 'comunicado_id', string="Comunicados")
    curso_id = fields.Many2one('pruebamjp.curso', string="Curso")

    def create_comunicado_for_all_users(self):
        try:
            users = self.env['res.users'].search([])
            self._create_comunicado_usuarios(users)
        except Exception as e:
            raise ValidationError(f"Error en create_comunicado_for_all_users: {e}")

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
        # Crear el comunicado normalmente
        record = super(Comunicado, self).create(vals)
        
        # Llamar a la función para enviar notificaciones push
        record._send_push_notifications(record.nombre, record.description)
        
        return record    

    def _send_push_notifications(self, title, body):
        #Enviar notificaciones push utilizando Firebase
        fcm_url = 'https://fcm.googleapis.com/v1/projects/agenda-e3371/messages:send'

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        service_account_path = os.path.join(base_dir, 'config_firebase', 'agenda-e3371-firebase-adminsdk-fbsvc-d80fd66917.json')

        # Crear credenciales OAuth 2.0 desde el archivo de cuenta de servicio
        credentials = Credentials.from_service_account_file(
            service_account_path,
            scopes=['https://www.googleapis.com/auth/firebase.messaging']
        )

        # Generar el token de acceso
        credentials.refresh(Request())
        access_token = credentials.token

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

        # Cuerpo de la solicitud
        payload = {
            "message": {
                "topic": "all",  # Enviar a todos los usuarios suscritos al tema 'all'
                "notification": {
                    "title": title,
                    "body": body,
                },
                "android": {
                    "priority": "HIGH",
                },
                "apns": {
                    "payload": {
                        "aps": {
                            "sound": "default"
                        }
                    }
                }
            }
        }

        # Hacer la solicitud
        try:
            response = requests.post(fcm_url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ValidationError(f"Error enviando notificación push: {e}")

    @api.depends('nombre') 
    def _compute_display_name(self): 
        for rec in self: 
            rec.display_name = f"{rec.nombre}"
