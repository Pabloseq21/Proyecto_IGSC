from datetime import datetime, timedelta
from collections import Counter
import database as db

# CALCULAR ZONAS DE RIESGO

def calcular_zonas_riesgo(radio=0.01):
    """
    Identifica zonas con alta concentración de robos
    radio: distancia en grados (0.01 ≈ 1km)
    """
    reportes = db.obtener_todos_reportes()
    
    if not reportes or len(reportes) < 2:
        return []
    
    zonas = []
    procesados = set()
    
    for i, reporte in enumerate(reportes):
        if i in procesados:
            continue
        
        lat1 = float(reporte['latitud'])
        lng1 = float(reporte['longitud'])
        
        # Buscar reportes cercanos (clustering simple)
        cluster = [reporte]
        procesados.add(i)
        
        for j, otro in enumerate(reportes):
            if j in procesados:
                continue
            
            lat2 = float(otro['latitud'])
            lng2 = float(otro['longitud'])
            
            # Distancia euclidiana aproximada
            distancia = ((lat1 - lat2)**2 + (lng1 - lng2)**2)**0.5
            
            if distancia < radio:
                cluster.append(otro)
                procesados.add(j)
        
        # Si hay 2+ robos cercanos = zona de riesgo
        if len(cluster) >= 2:
            lat_centro = sum(float(r['latitud']) for r in cluster) / len(cluster)
            lng_centro = sum(float(r['longitud']) for r in cluster) / len(cluster)
            
            tipos = [r['tipo_robo'] for r in cluster]
            tipo_comun = Counter(tipos).most_common(1)[0][0]
            
            zonas.append({
                'latitud': lat_centro,
                'longitud': lng_centro,
                'cantidad_robos': len(cluster),
                'nivel_riesgo': calcular_nivel_riesgo(len(cluster)),
                'tipo_mas_comun': tipo_comun,
                'radio_metros': int(radio * 111000)
            })
    
    return sorted(zonas, key=lambda x: x['cantidad_robos'], reverse=True)[:10]


def calcular_nivel_riesgo(cantidad):
    if cantidad >= 5:
        return 'ALTO'
    elif cantidad >= 3:
        return 'MEDIO'
    else:
        return 'BAJO'

# CALCULAR HORAS PELIGROSAS

def calcular_horas_peligrosas():
    reportes = db.obtener_todos_reportes()
    
    if not reportes:
        return []
    
    horas = {}
    for r in reportes:
        fecha = r['fecha_incidente']
        hora = fecha.hour
        horas[hora] = horas.get(hora, 0) + 1
    
    # Top 5 horas
    ordenado = sorted(horas.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return [
        {
            'hora': hora,
            'cantidad': cantidad,
            'rango': f"{hora:02d}:00 - {hora:02d}:59"
        }
        for hora, cantidad in ordenado
    ]

# CALCULAR DÍAS PELIGROSOS

def calcular_dias_peligrosos():
    """Identifica los días de la semana con más robos"""
    reportes = db.obtener_todos_reportes()
    
    if not reportes:
        return []
    
    dias_nombre = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    dias = {}
    
    for r in reportes:
        fecha = r['fecha_incidente']
        dia = fecha.weekday()  # 0=Lunes, 6=Domingo
        dias[dia] = dias.get(dia, 0) + 1
    
    ordenado = sorted(dias.items(), key=lambda x: x[1], reverse=True)
    
    return [
        {
            'dia': dias_nombre[dia],
            'cantidad': cantidad
        }
        for dia, cantidad in ordenado
    ]



# CALCULAR TIPO MÁS COMÚN

def calcular_tipo_mas_comun():
    reportes = db.obtener_todos_reportes()
    
    if not reportes:
        return None
    
    tipos = [r['tipo_robo'] for r in reportes]
    contador = Counter(tipos)
    mas_comun = contador.most_common(1)[0]
    
    return {
        'tipo': mas_comun[0],
        'cantidad': mas_comun[1],
        'porcentaje': round((mas_comun[1] / len(reportes)) * 100, 1)
    }


# CALCULAR TENDENCIA

def calcular_tendencia():
    reportes = db.obtener_todos_reportes()
    
    if not reportes:
        return None
    
    ahora = datetime.now()
    hace_7_dias = ahora - timedelta(days=7)
    hace_14_dias = ahora - timedelta(days=14)
    
    semana_actual = sum(1 for r in reportes if r['fecha_creacion'] >= hace_7_dias)
    semana_anterior = sum(1 for r in reportes if hace_14_dias <= r['fecha_creacion'] < hace_7_dias)
    
    if semana_anterior == 0:
        cambio = 0
        tendencia = 'ESTABLE'
    else:
        cambio = round(((semana_actual - semana_anterior) / semana_anterior) * 100, 1)
        if cambio > 10:
            tendencia = 'AUMENTANDO'
        elif cambio < -10:
            tendencia = 'DISMINUYENDO'
        else:
            tendencia = 'ESTABLE'
    
    return {
        'semana_actual': semana_actual,
        'semana_anterior': semana_anterior,
        'cambio_porcentual': cambio,
        'tendencia': tendencia
    }

# GENERAR REPORTE COMPLETO

def generar_reporte_completo():
    
    print(" Generando predicciones...")
    
    return {
        'zonas_riesgo': calcular_zonas_riesgo(),
        'horas_peligrosas': calcular_horas_peligrosas(),
        'dias_peligrosos': calcular_dias_peligrosos(),
        'tipo_mas_comun': calcular_tipo_mas_comun(),
        'tendencia': calcular_tendencia(),
        'total_reportes': len(db.obtener_todos_reportes()),
        'fecha_generacion': datetime.now().isoformat()
    }

# PREDICCIÓN POR UBICACIÓN

def predecir_riesgo_ubicacion(latitud, longitud, radio=0.005):
    reportes = db.obtener_todos_reportes()
    
    if not reportes:
        return {'nivel_riesgo': 'DESCONOCIDO', 'reportes_cercanos': 0}
    
    # Contar reportes cercanos
    cercanos = 0
    for r in reportes:
        lat2 = float(r['latitud'])
        lng2 = float(r['longitud'])
        
        distancia = ((latitud - lat2)**2 + (longitud - lng2)**2)**0.5
        
        if distancia < radio:
            cercanos += 1
    
    return {
        'latitud': latitud,
        'longitud': longitud,
        'reportes_cercanos': cercanos,
        'nivel_riesgo': calcular_nivel_riesgo(cercanos),
        'radio_metros': int(radio * 111000)
    }

# TEST
if __name__ == '__main__':
    print(" Probando módulo de predicción...")
    
    reporte = generar_reporte_completo()
    
    print(f"\n Resultados:")
    print(f"   Zonas de riesgo: {len(reporte['zonas_riesgo'])}")
    print(f"   Horas peligrosas: {len(reporte['horas_peligrosas'])}")
    print(f"   Tendencia: {reporte['tendencia']['tendencia'] if reporte['tendencia'] else 'N/A'}")
    print(f"\n Módulo funcionando correctamente")