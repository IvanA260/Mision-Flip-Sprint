import requests
import json
import time
import random
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar configuración
load_dotenv()

# Configuración para FRESAS
CONFIG_FRESAS = {
    'temperatura_optima_min': 0.0,
    'temperatura_optima_max': 2.0,
    'temperatura_alerta': 4.0,
    'temperatura_critica': 6.0,
    'humedad_minima': 90.0,
    'aceleracion_maxima': 2.5
}

def generar_datos_fresas():
    """Genera datos realistas para transporte de fresas"""
    
    # Temperatura: normalmente entre 0-3°C, ocasionalmente más alta para simular problemas
    if random.random() < 0.05:  # 5% de probabilidad de problema
        temperatura = random.uniform(5.0, 8.0)
    else:
        temperatura = random.uniform(0.5, 3.0)
    
    # Humedad: normalmente 90-95%, ocasionalmente baja
    if random.random() < 0.03:  # 3% de probabilidad de humedad baja
        humedad = random.uniform(80.0, 85.0)
    else:
        humedad = random.uniform(90.0, 95.0)
    
    # Acelerómetro: normalmente bajo, ocasionalmente alto por golpes
    if random.random() < 0.02:  # 2% de probabilidad de golpe
        acelerometro_z = random.uniform(2.5, 4.0)
    else:
        acelerometro_z = random.uniform(0.5, 1.8)
    
    datos = {
        "id_envio": f"fresas_{random.randint(1000, 9999)}",
        "producto": "fresas",
        "timestamp": datetime.now().isoformat(),
        "temperatura": round(temperatura, 2),
        "humedad": round(humedad, 2),
        "acelerometro_z": round(acelerometro_z, 2),
        "latitud": 40.4168 + random.uniform(-0.01, 0.01),
        "longitud": -3.7038 + random.uniform(-0.01, 0.01),
        "estado": "normal"
    }
    
    # Determinar estado basado en los datos
    if datos['temperatura'] > CONFIG_FRESAS['temperatura_critica']:
        datos['estado'] = "critico"
    elif datos['temperatura'] > CONFIG_FRESAS['temperatura_alerta']:
        datos['estado'] = "alerta"
    elif datos['humedad'] < CONFIG_FRESAS['humedad_minima']:
        datos['estado'] = "alerta"
    elif datos['acelerometro_z'] > CONFIG_FRESAS['aceleracion_maxima']:
        datos['estado'] = "alerta"
    
    return datos

def enviar_datos(datos):
    """Envía datos automáticamente a Google Cloud Functions"""
    try:
        # URL de producción - NO CAMBIAR
        CLOUD_FUNCTION_URL = "https://europe-west1-green-delivery-fresas.cloudfunctions.net/process-telemetry"
        
        # Mostrar datos en consola
        print(f"📦 Envío: {datos['id_envio']}")
        print(f"🌡️  Temperatura: {datos['temperatura']}°C")
        print(f"💧 Humedad: {datos['humedad']}%")
        print(f"📊 Acelerómetro: {datos['acelerometro_z']}G")
        print(f"📍 Estado: {datos['estado']}")
        print(f"🕐 {datos['timestamp']}")
        
        # Enviar a Cloud Function
        response = requests.post(
            CLOUD_FUNCTION_URL,
            json=datos,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            estado_cloud = result.get('estado', 'desconocido')
            print(f"✅ Cloud: {result['message']} - Estado: {estado_cloud}")
            
            # Indicar si se envió alerta a Discord
            if estado_cloud in ['alerta', 'critico']:
                print(f" Alerta enviada a Discord")
                
        else:
            print(f" Error Cloud: {response.status_code} - {response.text}")
        
        print("-" * 50)
        return True
        
    except requests.exceptions.RequestException as e:
        print(f" Error de conexión: {e}")
        return False
    except Exception as e:
        print(f" Error inesperado: {e}")
        return False

def main():
    print(" SISTEMA GREEN DELIVERY - EN PRODUCCIÓN")
    print(" Monitoreo de fresas en tiempo real")
    print(" Enviando datos cada 5 segundos")
    print(" Alertas automáticas a Discord activadas")
    print("  Umbrales: Normal(0-4°C) | Alerta(4-6°C) | Crítico(>6°C)")
    print(" Presiona Ctrl+C para detener")
    print("=" * 50)
    
    try:
        while True:
            # Generar y enviar datos automáticamente
            datos = generar_datos_fresas()
            enviar_datos(datos)
            time.sleep(5)  # Esperar 5 segundos
            
    except KeyboardInterrupt:
        print("\n Sistema detenido")

if __name__ == "__main__":
    main()