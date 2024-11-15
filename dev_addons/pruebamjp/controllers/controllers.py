# -*- coding: utf-8 -*-
from odoo import http


class Pruebamjp(http.Controller):
    @http.route('/pruebamjp/pruebamjp', auth='public')
    def index(self, **kw):

        return "Hello, world"
    @http.route('/pruebamjp/pruebamjp/objects', auth='public')
    def list(self, **kw):
        return http.request.render('pruebamjp.listing', {
            'root': '/pruebamjp/pruebamjp',
            'objects': http.request.env['pruebamjp.pruebamjp'].search([]),
        })

    @http.route('/pruebamjp/pruebamjp/objects/<model("pruebamjp.pruebamjp"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('pruebamjp.object', {
            'object': obj
        })

