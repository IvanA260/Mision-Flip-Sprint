# 🌱 GreenDelivery - Sistema de Monitoreo IoT para Fresas 🍓🍓🍓

**Flip Sprint - Sistema especializado en alerta temprana para cadena de frío de FRESAS 🍓🍓🍓**
<img width="160" height="160" alt="image" src="https://github.com/user-attachments/assets/59a2457f-21c4-4075-a66e-c7f3f42a7b21" />



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

**Milestone Investigación de tecnologías cloud**
- Investigar AWS vs Google Cloud vs Azure
- Comparar límites gratuitos
- Decidir base de datos (Firestore vs DynamoDB)
- Elegir servicio de funciones (Cloud Functions vs Lambda)






## 🔔 Sistema de Alertas
- Alerta Temperatura: "Fresas a 4.5°C - Riesgo de maduración acelerada"
- Alerta Crítica: "Fresas a 7.2°C - Pérdida de firmeza inminente"
- Alerta Impacto: "Golpe detectado - Posible daño a fresas"

## 📊 KPIs de Calidad para Fresas
- % de envíos en condiciones óptimas (0-2°C)
- Tiempo acumulado en zona de riesgo (>4°C)
- Número de impactos críticos por envío
- Tasa de falsos positivos en alertas

