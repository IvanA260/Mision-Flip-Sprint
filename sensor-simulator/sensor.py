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
    """Envía datos a la nube (por ahora solo los muestra)"""
    try:
        print(f"📦 Envío: {datos['id_envio']}")
        print(f"🌡️  Temperatura: {datos['temperatura']}°C")
        print(f"💧 Humedad: {datos['humedad']}%")
        print(f"📊 Acelerómetro: {datos['acelerometro_z']}G")
        print(f"📍 Estado: {datos['estado']}")
        print(f"🕐 {datos['timestamp']}")
        print("-" * 50)
        
        # TODO: Aquí enviaremos a Google Cloud después
        return True
        
    except Exception as e:
        print(f" Error enviando datos: {e}")
        return False

def main():
    print(" Iniciando simulador de sensor para FRESAS...")
    print(" Simulando transporte en zona Madrid")
    print(" Enviando datos cada 5 segundos")
    print("=" * 50)
    
    try:
        while True:
            datos = generar_datos_fresas()
            enviar_datos(datos)
            time.sleep(5)  # Esperar 5 segundos
            
    except KeyboardInterrupt:
        print("\n Simulador detenido por el usuario")

if __name__ == "__main__":
    main()