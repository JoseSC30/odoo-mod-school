from odoo import http
from odoo.http import request
import json
from werkzeug.wrappers import Response
from functools import wraps

def cors_enable(orig_func):
    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        response = orig_func(*args, **kwargs)
        response.headers.extend({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
        })
        if request.httprequest.method == 'OPTIONS':
            return Response(status=200, headers=response.headers)
        return response
    return wrapper


class ApiController(http.Controller):

    @http.route('/api/login', type='http', auth='none', methods=['POST', 'OPTIONS'], csrf=False)
    @cors_enable
    def login(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data.decode('utf-8'))
            db = data.get('db')
            login = data.get('login')
            password = data.get('password')
            
            if not db or not login or not password:
                response_data = json.dumps({'error': 'Faltan credenciales'})
                return Response(response_data, status=400, mimetype='application/json')
            
            uid = request.session.authenticate(db, login, password)
            if uid:
                response_data = json.dumps({'uid': uid, 'session_token': request.session.sid})
                return Response(response_data, status=200, mimetype='application/json')
            else:
                response_data = json.dumps({'error': 'Autenticación fallida'})
                return Response(response_data, status=401, mimetype='application/json')
        except Exception as e:
            response_data = json.dumps({'error': str(e)})
            return Response(response_data, status=500, mimetype='application/json')
        

    @http.route('/api/test', type='http', auth='none', methods=['POST', 'OPTIONS'], csrf=False)
    @cors_enable
    def test_endpoint(self, **kwargs):
        print("Received data:", request.httprequest.data)  # Agregar esta línea para depurar
        data = json.loads(request.httprequest.data.decode('utf-8'))
        auth_result = self.relogear(data)

        dataExtra = {
            'message': 'Este es un endpoint de prueba',
            'user': request.env.user.name,
            'extra_info': 'Aquí puedes añadir más datos como desees'
        }

        combined_data = {**auth_result, **dataExtra}

        if 'error' in auth_result:
            response_data = json.dumps(combined_data)
            return Response(response_data, status=auth_result['status'], mimetype='application/json')
        else:
            response_data = json.dumps(combined_data)
            return Response(response_data, status=200, mimetype='application/json')


    @staticmethod
    def relogear(data):
        try:
            db = data.get('db')
            login = data.get('login')
            password = data.get('password')

            if not db or not login or not password:
                return {'error': 'Faltan credenciales', 'status': 400}

            uid = request.session.authenticate(db, login, password)
            if uid:
                return {'uid': uid, 'session_token': request.session.sid, 'status': 200}
            else:
                return {'error': 'Autenticación fallida', 'status': 401}
        except Exception as e:
            return {'error': str(e),'status':500}