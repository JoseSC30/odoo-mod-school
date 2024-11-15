from odoo import http
from odoo.http import request
import json

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
