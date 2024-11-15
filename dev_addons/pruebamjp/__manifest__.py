# -*- coding: utf-8 -*-
{
    'name': "pruebamjp",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/curso.xml',
        'views/materia.xml',
        'views/ciclo.xml',
        'views/gestion.xml',
        'views/modalidad.xml',
        'views/profesor.xml',
        'views/estudiante.xml',
        'views/tutor.xml',
        'views/horario.xml',
        'views/curso_materia.xml',
        'views/estudiante_tutor.xml',
        'views/inscripcion.xml',
        'views/nota.xml',
        'views/subnota.xml',
        'views/mensualidad.xml',
        'views/comunicado.xml',
        'views/comunicado_usuario.xml',
        'views/asistencia.xml',

        
        
              




    ],
    'assets': {
        'web.assets_backend': [
            'pruebamjp/static/src/css/styles.css',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

