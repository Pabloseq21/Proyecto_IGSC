import os
class Config:
    """
    Clase de configuración principal
    Contiene todas las variables de configuración de la aplicación
    """
    
    # Host donde está corriendo PostgreSQL
    DB_HOST = 'localhost'
    
    # Puerto de PostgreSQL (por defecto es 5432)
    DB_PORT = '5432'
    
    # Nombre de la base de datos que creamos
    DB_NAME = 'reportes_robos'
    
    # Usuario de PostgreSQL
    DB_USER = 'postgres'
    
    DB_PASSWORD = '130521'  
    
    # CONFIGURACIÓN DE FLASK
    
    # Clave secreta para sesiones 
    SECRET_KEY = 'mi-clave-secreta-proyecto-robos-2024'
    
    # Modo debug (True = muestra errores detallados, False = producción)
    DEBUG = True
    
    # CONFIGURACIÓN DE CORS
    
    CORS_ORIGINS = '*'
    
    JSON_SORT_KEYS = False
    
    # Zona horaria
    TIMEZONE = 'America/Bogota'
    
    # Número máximo de resultados por página (para paginación futura)
    MAX_RESULTS_PER_PAGE = 100

# Mensaje de confirmación al cargar el módulo
print("=" * 60)
print("Configuración cargada correctamente")
print("=" * 60)
print(f"Base de datos:")
print(f"   - Nombre: {Config.DB_NAME}")
print(f"   - Host: {Config.DB_HOST}")
print(f"   - Puerto: {Config.DB_PORT}")
print(f"   - Usuario: {Config.DB_USER}")
print(f"   - Password: {'*' * len(Config.DB_PASSWORD)} (oculta)")
print("=" * 60)
print(f"Flask:")
print(f"   - Debug mode: {Config.DEBUG}")
print(f"   - CORS: {Config.CORS_ORIGINS}")
print("=" * 60)