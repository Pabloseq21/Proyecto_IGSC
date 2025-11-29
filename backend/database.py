import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

# FUNCIÓN DE CONEXIÓN

def get_connection():
    """Obtiene una conexión a la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

# FUNCIONES PARA USUARIOS

def crear_usuario(nombre, email, telefono, password_hash):
    """Crea un nuevo usuario en la base de datos"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            INSERT INTO usuarios (nombre, email, telefono, password_hash)
            VALUES (%s, %s, %s, %s)
            RETURNING *
        """, (nombre, email, telefono, password_hash))
        
        nuevo_usuario = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"Usuario creado: {nuevo_usuario['email']}")
        return nuevo_usuario
    except psycopg2.errors.UniqueViolation:
        print(f" El email {email} ya está registrado")
        return None
    except Exception as e:
        print(f" Error creando usuario: {e}")
        return None

def obtener_usuario_por_email(email):
    """Obtiene un usuario por su email"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT * FROM usuarios WHERE email = %s
        """, (email,))
        
        usuario = cur.fetchone()
        cur.close()
        conn.close()
        
        return usuario
    except Exception as e:
        print(f"Error obteniendo usuario: {e}")
        return None

def obtener_usuario_por_id(usuario_id):
    """Obtiene un usuario por su ID"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT id, nombre, email, telefono, fecha_registro, activo
            FROM usuarios WHERE id = %s
        """, (usuario_id,))
        
        usuario = cur.fetchone()
        cur.close()
        conn.close()
        
        return usuario
    except Exception as e:
        print(f" Error obteniendo usuario: {e}")
        return None

def obtener_todos_usuarios():
    """Obtiene todos los usuarios de la base de datos"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT id, nombre, email, telefono, fecha_registro, activo
            FROM usuarios
            ORDER BY fecha_registro DESC
        """)
        
        usuarios = cur.fetchall()
        cur.close()
        conn.close()
        
        return usuarios
    except Exception as e:
        print(f" Error obteniendo usuarios: {e}")
        return []

# FUNCIONES PARA REPORTES

def crear_reporte(usuario_id, tipo_robo, descripcion, latitud, longitud, fecha_incidente, barrio=None):
    """Crea un nuevo reporte en la base de datos"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            INSERT INTO reportes 
            (usuario_id, tipo_robo, descripcion, latitud, longitud, fecha_incidente, barrio)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (usuario_id, tipo_robo, descripcion, latitud, longitud, fecha_incidente, barrio))
        
        nuevo_reporte = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        print(f" Reporte creado: ID {nuevo_reporte['id']} por usuario {usuario_id}")
        return nuevo_reporte
    except Exception as e:
        print(f" Error creando reporte: {e}")
        return None

def obtener_todos_reportes():
    """Obtiene todos los reportes de la base de datos"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT 
                id, 
                usuario_id,
                tipo_robo, 
                descripcion, 
                latitud, 
                longitud, 
                fecha_incidente, 
                fecha_creacion,
                barrio
            FROM reportes 
            ORDER BY fecha_creacion DESC
        """)
        reportes = cur.fetchall()
        cur.close()
        conn.close()
        return reportes
    except Exception as e:
        print(f" Error obteniendo reportes: {e}")
        return []

def obtener_reportes_con_usuarios():
    """Obtiene todos los reportes con información del usuario que los creó"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT 
                r.id,
                r.usuario_id,
                r.tipo_robo,
                r.descripcion,
                r.latitud,
                r.longitud,
                r.fecha_incidente,
                r.fecha_creacion,
                r.barrio,
                u.nombre AS usuario_nombre,
                u.email AS usuario_email,
                u.telefono AS usuario_telefono
            FROM reportes r
            INNER JOIN usuarios u ON r.usuario_id = u.id
            ORDER BY r.fecha_creacion DESC
        """)
        
        reportes = cur.fetchall()
        cur.close()
        conn.close()
        
        return reportes
    except Exception as e:
        print(f" Error obteniendo reportes con usuarios: {e}")
        return []

def obtener_reportes_por_usuario(usuario_id):
    """Obtiene todos los reportes de un usuario específico"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT *
            FROM reportes
            WHERE usuario_id = %s
            ORDER BY fecha_creacion DESC
        """, (usuario_id,))
        
        reportes = cur.fetchall()
        cur.close()
        conn.close()
        
        return reportes
    except Exception as e:
        print(f" Error obteniendo reportes del usuario: {e}")
        return []

def obtener_reporte_por_id(reporte_id):
    """Obtiene un reporte específico por su ID"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT 
                r.*,
                u.nombre AS usuario_nombre,
                u.email AS usuario_email
            FROM reportes r
            INNER JOIN usuarios u ON r.usuario_id = u.id
            WHERE r.id = %s
        """, (reporte_id,))
        
        reporte = cur.fetchone()
        cur.close()
        conn.close()
        
        return reporte
    except Exception as e:
        print(f" Error obteniendo reporte: {e}")
        return None

# FUNCIONES PARA ESTADÍSTICAS

def obtener_estadisticas():
    """Obtiene estadísticas generales de los reportes"""
    conn = get_connection()
    if not conn:
        return {}
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Total de reportes
        cur.execute("SELECT COUNT(*) as total FROM reportes")
        total = cur.fetchone()['total']
        
        # Total de usuarios
        cur.execute("SELECT COUNT(*) as total_usuarios FROM usuarios")
        total_usuarios = cur.fetchone()['total_usuarios']
        
        # Reportes por tipo
        cur.execute("""
            SELECT tipo_robo, COUNT(*) as cantidad 
            FROM reportes 
            GROUP BY tipo_robo
            ORDER BY cantidad DESC
        """)
        por_tipo = cur.fetchall()
        
        # Reportes de hoy
        cur.execute("""
            SELECT COUNT(*) as hoy 
            FROM reportes 
            WHERE DATE(fecha_creacion) = CURRENT_DATE
        """)
        hoy = cur.fetchone()['hoy']
        
        # Reportes de esta semana
        cur.execute("""
            SELECT COUNT(*) as semana
            FROM reportes 
            WHERE fecha_creacion >= CURRENT_DATE - INTERVAL '7 days'
        """)
        semana = cur.fetchone()['semana']
        
        # Usuario con más reportes
        cur.execute("""
            SELECT 
                u.nombre,
                u.email,
                COUNT(r.id) as total_reportes
            FROM usuarios u
            LEFT JOIN reportes r ON u.id = r.usuario_id
            GROUP BY u.id, u.nombre, u.email
            ORDER BY total_reportes DESC
            LIMIT 1
        """)
        usuario_mas_activo = cur.fetchone()
        
        cur.close()
        conn.close()
        
        return {
            'total_reportes': total,
            'total_usuarios': total_usuarios,
            'reportes_hoy': hoy,
            'reportes_semana': semana,
            'por_tipo': por_tipo,
            'usuario_mas_activo': usuario_mas_activo
        }
    except Exception as e:
        print(f" Error obteniendo estadísticas: {e}")
        return {}

# FUNCIONES AUXILIARES

def eliminar_reporte(reporte_id):
    """Elimina un reporte por su ID"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM reportes WHERE id = %s", (reporte_id,))
        conn.commit()
        eliminado = cur.rowcount > 0
        cur.close()
        conn.close()
        
        if eliminado:
            print(f" Reporte {reporte_id} eliminado")
        return eliminado
    except Exception as e:
        print(f" Error eliminando reporte: {e}")
        return False

def actualizar_usuario(usuario_id, nombre=None, telefono=None):
    """Actualiza la información de un usuario"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        updates = []
        params = []
        
        if nombre:
            updates.append("nombre = %s")
            params.append(nombre)
        if telefono:
            updates.append("telefono = %s")
            params.append(telefono)
        
        if not updates:
            return None
        
        params.append(usuario_id)
        query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id = %s RETURNING *"
        
        cur.execute(query, params)
        usuario_actualizado = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
    
        print(f" Usuario {usuario_id} actualizado")
        return usuario_actualizado
    except Exception as e:
        print(f" Error actualizando usuario: {e}")
        return None

# TEST DE CONEXIÓN

if __name__ == "__main__":
    print(" Probando conexión a la base de datos...")
    
    conn = get_connection()
    if conn:
        print(" Conexión exitosa")
        conn.close()
    else:
        print(" No se pudo conectar")