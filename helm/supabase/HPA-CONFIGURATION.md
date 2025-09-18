# 📊 HPA Configuration Summary

## 🎯 **Configuración de Autoscaling Optimizada**

Todos los servicios inician con **1 réplica** por defecto y escalan automáticamente basado en CPU.

### 📈 **Configuración por Servicio:**

| Servicio | Min Replicas | Max Replicas | CPU Target | Justificación |
|----------|-------------|-------------|------------|---------------|
| **Studio** | 1 | 3 | 80% | Dashboard web - tráfico moderado |
| **Auth** | 1 | 5 | 70% | Crítico - alta demanda de autenticación |
| **REST** | 1 | 8 | 70% | API principal - mayor escalado |
| **Realtime** | 1 | 5 | 70% | WebSockets - carga variable |
| **Meta** | 1 | 3 | 80% | Metadata DB - uso estable |
| **Storage** | 1 | 4 | 70% | File uploads - carga media |
| **Imgproxy** | 1 | 3 | 80% | Procesamiento de imágenes |
| **Kong** | 1 | 3 | 70% | API Gateway - entrada principal |
| **Analytics** | 1 | 3 | 80% | Logs - carga estable |
| **Vector** | 1 | 2 | 80% | Log collection - baja carga |
| **Functions** | 1 | 5 | 80% | Edge functions - escalado dinámico |

### 🔧 **Recursos por Servicio:**

#### **Servicios Críticos (Mayor CPU/Memoria):**
- **Auth, REST, Realtime, Storage, Kong**: 200m-1000m CPU, 256-512Mi RAM

#### **Servicios Ligeros:**
- **Studio, Meta, Analytics, Functions**: 100m-500m CPU, 128-256Mi RAM

#### **Servicios Especializados:**
- **Imgproxy, Vector**: Configuración específica para su carga de trabajo

### ⚡ **Ventajas de esta Configuración:**

1. **💰 Costo Optimizado**: Inicia con mínimos recursos
2. **🚀 Escalado Automático**: Responde a demanda real
3. **🛡️ Alta Disponibilidad**: Múltiples réplicas bajo carga
4. **⚖️ Balance Perfecto**: Entre rendimiento y costo

### 📊 **Métricas de Escalado:**

- **CPU Target**: 70-80% (permite margen para picos)
- **Escalado Progresivo**: De 1 a máximo basado en demanda
- **Servicios Críticos**: Mayor capacidad de escalado (REST: hasta 8 replicas)

### 🎛️ **Personalización:**

Para ajustar el escalado, modifica en `values-aws.yaml`:

```yaml
serviceName:
  autoscaling:
    enabled: true
    minReplicas: 1        # Mínimo siempre 1
    maxReplicas: X        # Ajustar según necesidad
    targetCPUUtilizationPercentage: Y  # 70-80%
```

Esta configuración proporciona un balance óptimo entre costo y rendimiento! 🎯
