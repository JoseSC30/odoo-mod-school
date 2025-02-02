from odoo import http
from odoo.http import request
import json

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import requests
import os

class ComunicadoController(http.Controller):

    @http.route('/api/comunicados/general', auth='user', type='http', methods=['GET'], csrf=False)
    def get_comunicados_general(self, **kwargs):
        comunicados = request.env['pruebamjp.comunicado_usuario'].search([('usuario_recibe_id', 'in', request.env['res.users'].search([]).ids)])
        data = [{
            'nombre': com.comunicado_id.nombre,
            'descripcion': com.comunicado_id.description,
            'fecha': com.comunicado_id.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            'visto': com.visto
        } for com in comunicados]
        # data2 = [{
        #     'nombre': 'MArcelo-123',
        #     'cancion': 'submarino amarrillo'
        # } for com in comunicados]
        # return request.make_response(json.dumps(data2), headers=[('Content-Type', 'application/json')])
        return request.make_response(json.dumps(data), headers=[('Content-Type', 'application/json')])

    # -----
    @http.route('/api/comunicados/holamundo', auth='none', type='http', methods=['GET'], csrf=False)
    def get_holamundo(self, **kwargs):
        data = [{
            'nombre': 'Marcelo',
            'cancion': 'submarino amarrillo'
        }]
        return request.make_response(json.dumps(data), headers=[('Content-Type', 'application/json')])
    # -----


    # @http.route('/api/comunicados/curso/<int:curso_id>', auth='user', type='http', methods=['GET'], csrf=False)
    # def get_comunicados_curso(self, curso_id, **kwargs):
    #     curso = request.env['pruebamjp.curso'].browse(curso_id)
    #     if not curso.exists():
    #         return request.make_response(json.dumps({'error': 'Curso no encontrado'}), status=404)

    #     tutores_ids = [inscripcion.estudiante_id.estudiante_tutor_ids.tutor_id.usuario_id.id for inscripcion in curso.inscripcion_ids]
    #     comunicados = request.env['pruebamjp.comunicado_usuario'].search([('usuario_recibe_id', 'in', tutores_ids)])

    #     data = [{
    #         'nombre': com.comunicado_id.nombre,
    #         'descripcion': com.comunicado_id.description,
    #         'fecha': com.comunicado_id.fecha.strftime("%Y-%m-%d %H:%M:%S"),
    #         'visto': com.visto
    #     } for com in comunicados]
    #     return request.make_response(json.dumps(data), headers=[('Content-Type', 'application/json')])


    # @http.route('/api/comunicados/tutor/<int:tutor_id>', auth='user', type='http', methods=['GET'], csrf=False)
    # def get_comunicados_tutor(self, tutor_id, **kwargs):
    #     tutor = request.env['pruebamjp.tutor'].browse(tutor_id)
    #     if not tutor.exists():
    #         return request.make_response(json.dumps({'error': 'Tutor no encontrado'}), status=404)

    #     comunicados = request.env['pruebamjp.comunicado_usuario'].search([('usuario_recibe_id', '=', tutor.usuario_id.id)])

    #     data = [{
    #         'nombre': com.comunicado_id.nombre,
    #         'descripcion': com.comunicado_id.description,
    #         'fecha': com.comunicado_id.fecha.strftime("%Y-%m-%d %H:%M:%S"),
    #         'visto': com.visto
    #     } for com in comunicados]
    #     return request.make_response(json.dumps(data), headers=[('Content-Type', 'application/json')])

    @http.route('/api/comunicados/visto/<int:comunicado_usuario_id>', auth='user', type='http', methods=['POST'], csrf=False)
    def marcar_como_visto(self, comunicado_usuario_id, **kwargs):
        comunicado_usuario = request.env['pruebamjp.comunicado_usuario'].browse(comunicado_usuario_id)
        if not comunicado_usuario.exists():
            return request.make_response(json.dumps({'error': 'Comunicado no encontrado'}), status=404)

        comunicado_usuario.write({'visto': 'si'})
        return request.make_response(json.dumps({'success': 'Comunicado marcado como visto'}), headers=[('Content-Type', 'application/json')])


    #-----------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------

    # funcion para crear comunicado y enviar a los usuariarios notificaciones push
    @http.route('/api/comunicados/general', auth='user', type='http', methods=['POST'], csrf=False)
    def crear_comunicado(self, **kwargs):
        try:
            # Parsear datos del cuerpo de la solicitud
            data = json.loads(request.httprequest.data)
            nombre = data.get('nombre')
            descripcion = data.get('descripcion')
            fecha = data.get('fecha')

            # Validar datos
            if not nombre or not descripcion or not fecha:
                return request.make_response(
                    json.dumps({'error': 'Faltan datos necesarios'}),
                    status=400
                )

            # Crear el comunicado
            comunicado = request.env['pruebamjp.comunicado'].create({
                'nombre': nombre,
                'description': descripcion,
                'fecha': fecha,
            })

            # Obtener todos los usuarios a quienes se asignará el comunicado
            usuarios = request.env['res.users'].search([])

            # Crear registros en 'pruebamjp.comunicado_usuario'
            comunicado_usuario_model = request.env['pruebamjp.comunicado_usuario']
            for usuario in usuarios:
                comunicado_usuario_model.create({
                    'visto': True,  # Asegúrate de que el campo 'visto' sea False por defecto
                    'comunicado_id': comunicado.id,
                    'usuario_recibe_id': usuario.id,
                })

            # Enviar notificación a los dispositivos
            self._send_push_notifications(nombre, descripcion)
    

            # Responder con éxito
            return request.make_response(
                json.dumps({
                    'success': 'Comunicado creado y asignado a usuarios',
                    'comunicado_id': comunicado.id
                }),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            # Manejar excepciones y registrar errores
            return request.make_response(
                json.dumps({'error': str(e)}),
                status=500
            )
        



    def _send_push_notifications(self, title, body):
    
        # Enviar notificaciones push utilizando Firebase Cloud Messaging (API v1)
        fcm_url = 'https://fcm.googleapis.com/v1/projects/agenda-e3371/messages:send'

        # Obtén la ruta absoluta al archivo de credenciales
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

        try:
            response = requests.post(fcm_url, headers=headers, json=payload)
            response.raise_for_status()
            #print(response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            request.env.cr.rollback()
            raise Exception(f"Error enviando notificación: {e}")


    
