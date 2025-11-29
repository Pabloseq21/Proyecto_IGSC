from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import database as db

# CONFIGURACIÓN DE FLASK

app = Flask(__name__)
CORS(app)  # Permite que el frontend hable con el backend

@app.route('/')
def home():
    """Página de inicio - Documentación de la API"""
    return jsonify({
        'mensaje': 'API de Sistema de Reportes de Robos',
        'version': '1.0',
        'estado': 'activo',
        'endpoints': {
            'GET /': 'Documentación de la API',
            'GET /api/reportes': 'Obtener todos los reportes',
            'POST /api/reportes': 'Crear un nuevo reporte',
            'GET /api/reportes/<id>': 'Obtener un reporte específico',
            'DELETE /api/reportes/<id>': 'Eliminar un reporte',
            'GET /api/reportes-con-usuarios': 'Obtener reportes con info de usuarios',
            'GET /api/usuarios': 'Obtener todos los usuarios',
            'POST /api/usuarios': 'Crear un nuevo usuario',
            'GET /api/usuarios/<id>': 'Obtener un usuario específico',
            'GET /api/usuarios/<id>/reportes': 'Obtener reportes de un usuario',
            'GET /api/estadisticas': 'Obtener estadísticas generales'
        }
    })

# RUTAS PARA REPORTES
@app.route('/api/reportes', methods=['GET'])
def obtener_reportes():
    """Obtener todos los reportes"""
    try:
        reportes = db.obtener_todos_reportes()
        
        # Convertir a formato JSON
        reportes_json = []
        for reporte in reportes:
            reporte_dict = dict(reporte)
            reporte_dict['latitud'] = float(reporte_dict['latitud'])
            reporte_dict['longitud'] = float(reporte_dict['longitud'])
            reporte_dict['fecha_incidente'] = reporte_dict['fecha_incidente'].isoformat()
            reporte_dict['fecha_creacion'] = reporte_dict['fecha_creacion'].isoformat()
            reportes_json.append(reporte_dict)
        
        return jsonify({
            'success': True,
            'data': reportes_json,
            'total': len(reportes_json)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/reportes', methods=['POST'])
def crear_reporte():
    """Crear un nuevo reporte"""
    try:
        datos = request.get_json()
        
        # Validar datos requeridos
        campos_requeridos = ['usuario_id', 'tipo_robo', 'descripcion', 'latitud', 'longitud', 'fecha_incidente']
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({
                    'success': False,
                    'error': f'Falta el campo requerido: {campo}'
                }), 400
        
        # Crear el reporte
        nuevo_reporte = db.crear_reporte(
            usuario_id=int(datos['usuario_id']),
            tipo_robo=datos['tipo_robo'],
            descripcion=datos['descripcion'],
            latitud=float(datos['latitud']),
            longitud=float(datos['longitud']),
            fecha_incidente=datos['fecha_incidente'],
            barrio=datos.get('barrio')
        )
        
        if nuevo_reporte:
            # Convertir para JSON
            reporte_dict = dict(nuevo_reporte)
            reporte_dict['latitud'] = float(reporte_dict['latitud'])
            reporte_dict['longitud'] = float(reporte_dict['longitud'])
            reporte_dict['fecha_incidente'] = reporte_dict['fecha_incidente'].isoformat()
            reporte_dict['fecha_creacion'] = reporte_dict['fecha_creacion'].isoformat()
            
            return jsonify({
                'success': True,
                'data': reporte_dict,
                'mensaje': 'Reporte creado exitosamente'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo crear el reporte'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/reportes/<int:reporte_id>', methods=['GET'])
def obtener_reporte(reporte_id):
    """Obtener un reporte específico"""
    try:
        reporte = db.obtener_reporte_por_id(reporte_id)
        
        if reporte:
            reporte_dict = dict(reporte)
            reporte_dict['latitud'] = float(reporte_dict['latitud'])
            reporte_dict['longitud'] = float(reporte_dict['longitud'])
            reporte_dict['fecha_incidente'] = reporte_dict['fecha_incidente'].isoformat()
            reporte_dict['fecha_creacion'] = reporte_dict['fecha_creacion'].isoformat()
            
            return jsonify({
                'success': True,
                'data': reporte_dict
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Reporte no encontrado'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/reportes/<int:reporte_id>', methods=['DELETE'])
def eliminar_reporte(reporte_id):
    """Eliminar un reporte"""
    try:
        eliminado = db.eliminar_reporte(reporte_id)
        
        if eliminado:
            return jsonify({
                'success': True,
                'mensaje': f'Reporte {reporte_id} eliminado exitosamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Reporte no encontrado'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/reportes-con-usuarios', methods=['GET'])
def obtener_reportes_con_info_usuarios():
    """Obtener reportes con información completa de usuarios"""
    try:
        reportes = db.obtener_reportes_con_usuarios()
        
        reportes_json = []
        for reporte in reportes:
            reporte_dict = dict(reporte)
            reporte_dict['latitud'] = float(reporte_dict['latitud'])
            reporte_dict['longitud'] = float(reporte_dict['longitud'])
            reporte_dict['fecha_incidente'] = reporte_dict['fecha_incidente'].isoformat()
            reporte_dict['fecha_creacion'] = reporte_dict['fecha_creacion'].isoformat()
            reportes_json.append(reporte_dict)
        
        return jsonify({
            'success': True,
            'data': reportes_json,
            'total': len(reportes_json)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# RUTAS PARA USUARIOS

@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    """Obtener todos los usuarios"""
    try:
        usuarios = db.obtener_todos_usuarios()
        
        usuarios_json = []
        for usuario in usuarios:
            usuario_dict = dict(usuario)
            usuario_dict['fecha_registro'] = usuario_dict['fecha_registro'].isoformat()
            usuarios_json.append(usuario_dict)
        
        return jsonify({
            'success': True,
            'data': usuarios_json,
            'total': len(usuarios_json)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/usuarios', methods=['POST'])
def crear_nuevo_usuario():
    """Crear un nuevo usuario"""
    try:
        datos = request.get_json()
        
        # Validar campos requeridos
        if not datos.get('nombre') or not datos.get('email'):
            return jsonify({
                'success': False,
                'error': 'Nombre y email son requeridos'
            }), 400
        
        # Por ahora usamos un hash simple (en producción usar bcrypt)
        password = datos.get('password', 'password123')
        password_hash = f"hash_{password}"
        
        nuevo_usuario = db.crear_usuario(
            nombre=datos['nombre'],
            email=datos['email'],
            telefono=datos.get('telefono'),
            password_hash=password_hash
        )
        
        if nuevo_usuario:
            usuario_dict = dict(nuevo_usuario)
            usuario_dict['fecha_registro'] = usuario_dict['fecha_registro'].isoformat()
            # No devolver el password_hash
            del usuario_dict['password_hash']
            
            return jsonify({
                'success': True,
                'data': usuario_dict,
                'mensaje': 'Usuario creado exitosamente'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo crear el usuario. Es posible que el email ya esté registrado.'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/usuarios/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    """Obtener un usuario específico"""
    try:
        usuario = db.obtener_usuario_por_id(usuario_id)
        
        if usuario:
            usuario_dict = dict(usuario)
            usuario_dict['fecha_registro'] = usuario_dict['fecha_registro'].isoformat()
            
            return jsonify({
                'success': True,
                'data': usuario_dict
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/usuarios/<int:usuario_id>/reportes', methods=['GET'])
def obtener_reportes_usuario(usuario_id):
    """Obtener todos los reportes de un usuario específico"""
    try:
        reportes = db.obtener_reportes_por_usuario(usuario_id)
        
        reportes_json = []
        for reporte in reportes:
            reporte_dict = dict(reporte)
            reporte_dict['latitud'] = float(reporte_dict['latitud'])
            reporte_dict['longitud'] = float(reporte_dict['longitud'])
            reporte_dict['fecha_incidente'] = reporte_dict['fecha_incidente'].isoformat()
            reporte_dict['fecha_creacion'] = reporte_dict['fecha_creacion'].isoformat()
            reportes_json.append(reporte_dict)
        
        return jsonify({
            'success': True,
            'data': reportes_json,
            'total': len(reportes_json)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/usuarios/<int:usuario_id>', methods=['PUT'])
def actualizar_usuario(usuario_id):
    """Actualizar información de un usuario"""
    try:
        datos = request.get_json()
        
        usuario_actualizado = db.actualizar_usuario(
            usuario_id=usuario_id,
            nombre=datos.get('nombre'),
            telefono=datos.get('telefono')
        )
        
        if usuario_actualizado:
            usuario_dict = dict(usuario_actualizado)
            usuario_dict['fecha_registro'] = usuario_dict['fecha_registro'].isoformat()
            del usuario_dict['password_hash']
            
            return jsonify({
                'success': True,
                'data': usuario_dict,
                'mensaje': 'Usuario actualizado exitosamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado o no se pudo actualizar'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# RUTAS PARA ESTADÍSTICAS

@app.route('/api/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """Obtener estadísticas generales del sistema"""
    try:
        stats = db.obtener_estadisticas()
        
        # Convertir por_tipo a formato JSON serializable
        if 'por_tipo' in stats:
            stats['por_tipo'] = [dict(item) for item in stats['por_tipo']]
        
        # Convertir usuario_mas_activo
        if stats.get('usuario_mas_activo'):
            stats['usuario_mas_activo'] = dict(stats['usuario_mas_activo'])
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# MANEJO DE ERRORES

@app.errorhandler(404)
def not_found(error):
    """Manejo de rutas no encontradas"""
    return jsonify({
        'success': False,
        'error': 'Ruta no encontrada'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores internos del servidor"""
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    }), 500

# INICIAR SERVIDOR=

if __name__ == '__main__':
    print('=' * 50)
    print('Iniciando servidor Flask...')
    print('=' * 50)
    print('Servidor corriendo en: http://localhost:5000')
    print('Documentación API: http://localhost:5000/')
    print('=' * 50)
    print('Rutas disponibles:')
    print('   GET  /api/reportes')
    print('   POST /api/reportes')
    print('   GET  /api/reportes/<id>')
    print('   DELETE /api/reportes/<id>')
    print('   GET  /api/reportes-con-usuarios')
    print('   GET  /api/usuarios')
    print('   POST /api/usuarios')
    print('   GET  /api/usuarios/<id>')
    print('   PUT  /api/usuarios/<id>')
    print('   GET  /api/usuarios/<id>/reportes')
    print('   GET  /api/estadisticas')
    print(' Presiona Ctrl+C para detener el servidor')
    print('=' * 50)
    
    app.run(debug=True, port=5000, host='0.0.0.0')