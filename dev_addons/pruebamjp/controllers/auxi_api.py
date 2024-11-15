# academic_management/controllers/auth_api.py
from odoo import http
from odoo.http import request
import json
from werkzeug.wrappers import Response
import jwt
import datetime
import logging

_logger = logging.getLogger(__name__)

CORS = "*"


class AuxiAPI(http.Controller):

    secret_key = "hola"


    def _response_with_cors(self, data, status=200):
        response = request.make_response(json.dumps(data), headers=[
            ("Content-Type", "application/json"),
            ("Access-Control-Allow-Origin", CORS),
        ])
        response.status_code = status
        return response


    @http.route("/api/estudiante/<int:estudiante>", auth="public", methods=["GET"], csrf=False)
    def get_subnotas_by_student(self, estudiante):
        token = request.httprequest.headers.get("Authorization")
        if not token:
            _logger.error("Token faltante en la solicitud")
            return self._response_with_cors({
                "error": "Token faltante",
                "success": False,
            }, 401)

        if token.startswith("Bearer "):
            token = token.split(" ")[1]  # Obtener solo el token, sin el prefijo 'Bearer '

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            user_id = payload.get("user_id")

            # Verificar que el usuario existe
            user = request.env["res.users"].sudo().browse(user_id)
            if not user:
                _logger.error("El usuario con ID %s no existe", user_id)
                return self._response_with_cors({
                    "error": "Usuario no autorizado",
                    "message": "El usuario no existe",
                    "success": False,
                }, 403)

            # Buscar la inscripción del estudiante
            estudianteb = request.env['pruebamjp.estudiante'].sudo().search([
                ('id', '=', int(estudiante))
            ], limit=1)

            if not estudianteb:
                return self._response_with_cors({
                    "error": " estudiante no encontrado",
                    "success": False,
                }, 404)
             # Buscar las subnotas relacionadas con la inscripción y filtrar por el campo 'numero'
            # subnotas = request.env['pruebamjp.subnota'].sudo().search([
            #     ('subinscripcion_id', '=', inscripcion.id)
            # ])

            estudiante_data = [{
                "id": estudianteb.id,
                "nombre": estudianteb.nombre,
                "apellido": estudianteb.apellido,
                "edad": estudianteb.edad,
            }]

            return self._response_with_cors({
                "success": True,
                "data": estudiante_data,
            })

        except jwt.ExpiredSignatureError:
            _logger.error("Token expirado")
            return self._response_with_cors({
                "error": "Token expirado",
                "success": False,
            }, 403)
        except jwt.InvalidTokenError:
            _logger.error("Token inválido")
            return self._response_with_cors({
                "error": "Token inválido",
                "success": False,
            }, 403)
        except Exception as e:
            _logger.exception("Error al procesar la solicitud: %s", str(e))
            return self._response_with_cors({
                "error": "Error Interno del Servidor",
                "message": str(e),
                "success": False,
            }, 500)
      