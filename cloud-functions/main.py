import functions_framework
from google.cloud import firestore
import json
from datetime import datetime
import requests
import os

# Configuración para fresas
CONFIG_FRESAS = {
    'temperatura_optima_min': 0.0,
    'temperatura_optima_max': 2.0,
    'temperatura_alerta': 6.0,        # ← CAMBIADO de 4.0 a 6.0
    'temperatura_critica': 10.0,      # ← CAMBIADO de 6.0 a 10.0
    'humedad_minima': 90.0,
    'aceleracion_maxima': 2.5
}

# CONFIGURACIÓN DISCORD - REEMPLAZA CON TU WEBHOOK REAL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1428286770444898379/FkE8x-LxcTyXRy23MCbuzgj9Ewz6nAVwcDFRq9nvKccEgJ5OUid2V1NDFKZmsH-XjyNE"

@functions_framework.http
def process_telemetry(request):
    """Función principal que procesa los datos del sensor de fresas"""
    
    # Configurar CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)
    
    headers = {'Access-Control-Allow-Origin': '*'}
    
    try:
        # Obtener datos del request
        request_json = request.get_json(silent=True)
        
        if not request_json:
            return json.dumps({
                'status': 'error',
                'message': 'No se recibieron datos JSON'
            }), 400, headers
        
        # Validar campos obligatorios
        required_fields = ['id_envio', 'temperatura', 'humedad', 'acelerometro_z', 'latitud', 'longitud']
        for field in required_fields:
            if field not in request_json:
                return json.dumps({
                    'status': 'error', 
                    'message': f'Campo obligatorio faltante: {field}'
                }), 400, headers
        
        # Añadir timestamp si no viene
        if 'timestamp' not in request_json:
            request_json['timestamp'] = datetime.now().isoformat()
        
        # Determinar estado
        estado = determinar_estado(request_json)
        request_json['estado'] = estado
        
        # Guardar en Firestore
        guardar_en_firestore(request_json)
        
        # Si es crítico o alerta, enviar notificación automática
        if estado in ['alerta', 'critico']:
            enviar_alerta_discord(request_json)
        
        # Respuesta exitosa
        return json.dumps({
            'status': 'success',
            'message': 'Datos procesados correctamente',
            'estado': estado,
            'id_envio': request_json['id_envio']
        }), 200, headers
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': f'Error procesando datos: {str(e)}'
        }), 500, headers

def determinar_estado(datos):
    """Determina el estado del envío basado en los umbrales de fresas"""
    
    if datos['temperatura'] > CONFIG_FRESAS['temperatura_critica']:
        return 'critico'
    
    if (datos['temperatura'] > CONFIG_FRESAS['temperatura_alerta'] or
        datos['humedad'] < CONFIG_FRESAS['humedad_minima'] or
        datos['acelerometro_z'] > CONFIG_FRESAS['aceleracion_maxima']):
        return 'alerta'
    
    return 'normal'

def guardar_en_firestore(datos):
    """Guarda los datos en Firestore"""
    try:
        # Configurar Firestore
        db = firestore.Client()
        
        # Crear referencia al documento
        doc_ref = db.collection('telemetria').document()
        
        # Preparar datos para guardar
        firestore_data = {
            'id_envio': datos['id_envio'],
            'producto': datos.get('producto', 'fresas'),
            'timestamp': datos['timestamp'],
            'temperatura': float(datos['temperatura']),
            'humedad': float(datos['humedad']),
            'acelerometro_z': float(datos['acelerometro_z']),
            'latitud': float(datos['latitud']),
            'longitud': float(datos['longitud']),
            'estado': datos['estado'],
            'procesado_en': datetime.now().isoformat()
        }
        
        # Guardar en Firestore
        doc_ref.set(firestore_data)
        
    except Exception as e:
        print(f"Error guardando en Firestore: {e}")
        raise

def enviar_alerta_discord(datos):
    """Envía una alerta automática a Discord cuando hay condiciones críticas"""
    try:
        # Determinar tipo de alerta y mensaje
        if datos['estado'] == 'critico':
            if datos['temperatura'] > CONFIG_FRESAS['temperatura_critica']:
                mensaje = f"🚨 **ALERTA CRÍTICA** - Temperatura elevada\n"
                mensaje += f"**Envío:** {datos['id_envio']}\n"
                mensaje += f"**Temperatura:** {datos['temperatura']}°C (Límite: {CONFIG_FRESAS['temperatura_critica']}°C)\n"
                mensaje += f"**Ubicación:** {datos['latitud']:.4f}, {datos['longitud']:.4f}\n"
                mensaje += f"**Hora:** {datos['timestamp'][11:19]}\n"
                mensaje += "**Acción requerida:** ¡Las fresas están en peligro! Revisar refrigeración inmediatamente."
                color = 16711680  # Rojo
                
        elif datos['estado'] == 'alerta':
            mensaje = f"⚠️ **ALERTA** - Condición de riesgo\n"
            mensaje += f"**Envío:** {datos['id_envio']}\n"
            
            if datos['temperatura'] > CONFIG_FRESAS['temperatura_alerta']:
                mensaje += f"**Temperatura:** {datos['temperatura']}°C (Límite: {CONFIG_FRESAS['temperatura_alerta']}°C)\n"
            elif datos['humedad'] < CONFIG_FRESAS['humedad_minima']:
                mensaje += f"**Humedad:** {datos['humedad']}% (Mínimo: {CONFIG_FRESAS['humedad_minima']}%)\n"
            elif datos['acelerometro_z'] > CONFIG_FRESAS['aceleracion_maxima']:
                mensaje += f"**Impacto:** {datos['acelerometro_z']}G (Máximo: {CONFIG_FRESAS['aceleracion_maxima']}G)\n"
            
            mensaje += f"**Ubicación:** {datos['latitud']:.4f}, {datos['longitud']:.4f}\n"
            mensaje += f"**Hora:** {datos['timestamp'][11:19]}\n"
            mensaje += "**Acción:** Monitorear situación."
            color = 16753920  # Naranja
            
        else:
            return  # No enviar alerta para estado normal
        
        # Preparar payload para Discord
        payload = {
            "content": " **GREEN DELIVERY - ALERTA**",
            "embeds": [
                {
                    "title": "🚨 Sistema de Monitoreo de Fresas",
                    "description": mensaje,
                    "color": color,
                    "footer": {
                        "text": "Sistema de Alertas Automáticas • GreenDelivery"
                    },
                    "timestamp": datos['timestamp']
                }
            ]
        }
        
        # Enviar a Discord automáticamente
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code != 204:
            print(f"Error enviando alerta a Discord: {response.status_code}")
            
    except Exception as e:
        print(f"Error en alerta Discord: {e}")

# Punto de entrada para Gen2
if __name__ == "__main__":
    functions_framework.start()