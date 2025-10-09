# 🍓🍓 GreenDelivery - Sistema de Monitoreo IoT para Fresas 🍓🍓

**🍓🍓 Flip Sprint - Sistema especializado en alerta temprana para cadena de frío de FRESAS 🍓🍓**



<img width="160" height="160" alt="image-removebg-preview (6)" src="https://github.com/user-attachments/assets/cea6e707-46e4-4d88-b908-767734b29b02" />




## 👥 Equipo
- Daniel del Molino
- Said Benjamin Velasquez  
- Ivan Araujo
- Alberto Salido

## 🎯 Objetivo del Proyecto
Desarrollar un sistema de monitoreo en tiempo real especializado en el transporte de fresas frescas, garantizando la cadena de frío (0-2°C) y detectando incidentes que puedan comprometer la calidad del producto.

## 🍓 Especificaciones Técnicas - Fresas

**Temperatura:**
- Óptimo: 0°C - 2°C
- Alerta: >4°C por más de 15 minutos
- Crítico: >6°C

**Humedad:**
- Óptimo: 90-95%
- Alerta: <85% por más de 30 minutos
- Crítico: <80%

**Impactos:**
- Normal: <2.0G
- Alerta: 2.0G-2.5G
- Crítico: >2.5G

## 🏗️ Arquitectura del Sistema
Edge (Sensor IoT) → Cloud Functions → Firestore → Dashboard & Alertas

## 🚀 Milestones del Proyecto

**Milestone 1: Configuración inicial del proyecto**
- Crear estructura de carpetas
- Configurar README.md principal
- Configurar .gitignore
- Establecer requirements.txt inicial
- Configurar project board

**Milestone 2: Investigación de tecnologías cloud**
- Investigar AWS vs Google Cloud vs Azure
- Comparar límites gratuitos
- Decidir base de datos (Firestore vs DynamoDB)
- Elegir servicio de funciones (Cloud Functions vs Lambda)

**Milestone 3: Desarrollo del simulador de sensor**
- Crear script Python en sensor-simulator/sensor.py
- Generar datos realistas: temperatura, humedad, ubicación, acelerómetro
- Implementar envío cada 5 segundos via HTTP POST
- Usar librería Faker para datos creíbles
- Formatear datos como JSON

**Milestone 4: Pruebas del simulador**
- Crear pruebas unitarias para generación de datos
- Verificar formatos de timestamp y tipos de datos
- Testear manejo de errores de red
- Documentar cómo ejecutar las pruebas

**Milestone 5: Configurar Cloud Functions**
- Crear función en Google Cloud Functions con trigger HTTP
- Configurar endpoint /api/telemetry
- Validar JSON recibido del sensor
- Implementar parsing de datos de telemetría
- Devolver respuesta apropiada

**Milestone 6: Configurar base de datos Firestore**
- Crear base de datos Firestore
- Diseñar schema
- Implementar conexión desde Cloud Function
- Crear índices necesarios
- Probar escritura y lectura de datos

**Milestone 7: Implementar lógica de detección**
- Implementar regla: temperatura > 8.0 → alerta
- Implementar regla: acelerometro_z > 3.0 → alerta
- Implementar regla: humedad < 20 → alerta (opcional)
- Guardar alertas en colección separada
- Probar lógica con datos de prueba
  (recuerda que esto son datos falsos solo para el readme,las verdaderas especificaciones de las metricas estan mas arriba)

**Milestone 8: Configurar notificaciones Slack/Discord**
- Crear webhook en Slack/Discord
- Modificar Cloud Function para enviar mensajes al webhook
- Formatear mensajes de alerta con información relevante
- Probar envío de notificaciones

**Milestone 9: Desarrollo del dashboard**
- Conectar Looker Studio a Firestore
- Crear visualización: mapa con última ubicación de envíos
- Crear gráfico de series temporales para temperatura
- Mostrar lista de alertas recientes
- Configurar actualización automática

**Milestone 10: Implementar KPIs de negocio**
- KPI: % de envíos en SLA (sin alertas críticas)
- KPI: Tiempo medio de detección (MTTD)
- KPI: % de falsos positivos
- Mostrar KPIs en dashboard
- Documentar cálculos de métricas

**Milestone 11: Implementar seguridad básica**
- Configurar variables de entorno para credenciales
- Validación de datos de entrada en Cloud Function
- Implementar reintentos con backoff exponencial
- Verificar que no hay credenciales en código
- Configurar permisos mínimos en cloud

**Milestone 12: Preparar presentación**
- Crear slides de arquitectura y decisiones
- Preparar guion para demo en vivo
- Asignar roles para la presentación
- Crear vídeo demo de 3-5 minutos
- Preparar documentación final



## 🔔 Sistema de Alertas
- Alerta Temperatura: "Fresas a 4.5°C - Riesgo de maduración acelerada"
- Alerta Crítica: "Fresas a 7.2°C - Pérdida de firmeza inminente"
- Alerta Impacto: "Golpe detectado - Posible daño a fresas"

## 📊 KPIs de Calidad para Fresas
- % de envíos en condiciones óptimas (0-2°C)
- Tiempo acumulado en zona de riesgo (>4°C)
- Número de impactos críticos por envío
- Tasa de falsos positivos en alertas


<img width="200" height="200" alt="image-removebg-preview (8)" src="https://github.com/user-attachments/assets/5aacbb0e-b3c6-4872-aa54-2f157ac1b3e6" />

