# Configuración de Base de Datos - Supabase Helm Chart

Este Helm chart soporta dos modos de configuración de base de datos:

## 1. Base de Datos Externa (Recomendado para Producción)

Para usar una base de datos externa como Amazon RDS:

```yaml
# values.yaml
db:
  enabled: false  # Deshabilitar DB interna
  external:
    host: "your-rds-endpoint.amazonaws.com"
    port: "5432"
    database: "postgres"
    username: "postgres"
    sslmode: "require"  # Configuración SSL para DB externa

# Usar External Secrets para credenciales
secret:
  db:
    enabled: true  # Habilitar External Secrets para DB
```

### Configuración con External Secrets (AWS Secrets Manager)

El chart está configurado para usar AWS Secrets Manager a través de External Secrets Operator:

```yaml
# Secret en AWS Secrets Manager: supabase/database
{
  "username": "your-db-user",
  "password": "your-db-password", 
  "database": "your-db-name",
  "host": "your-rds-endpoint.amazonaws.com"
}
```

## 2. Base de Datos Interna (Para Desarrollo/Testing)

Para usar la base de datos PostgreSQL incluida en el chart:

```yaml
# values.yaml
db:
  enabled: true  # Habilitar DB interna
  persistence:
    enabled: true
    size: 20Gi
  resources:
    requests:
      cpu: 500m
      memory: 1Gi
    limits:
      cpu: 2000m
      memory: 2Gi
  external:
    username: "postgres"
    password: "your-password"  # Contraseña para DB interna
    database: "postgres"

# Deshabilitar External Secrets para usar credenciales locales
secret:
  db:
    enabled: false  # Usar secreto local generado automáticamente
```

## Configuración SSL Automática

El chart configura automáticamente el modo SSL según el tipo de base de datos:

- **DB Interna**: `sslmode=disable` (conexiones locales)
- **DB Externa**: `sslmode=require` (por defecto, configurable)

## Variables de Entorno Generadas

El chart genera automáticamente las siguientes variables para todos los servicios:

- `DB_HOST`: Host de la base de datos
- `DB_PORT`: Puerto de la base de datos  
- `DB_SSL`: Modo SSL apropiado
- `DB_USER`: Usuario de la base de datos
- `DB_PASSWORD`: Contraseña de la base de datos
- `DB_NAME`: Nombre de la base de datos

## Migración entre Configuraciones

### De Externa a Interna

1. Cambiar `db.enabled: true`
2. Cambiar `secret.db.enabled: false`
3. Configurar credenciales en `db.external.password`
4. Realizar upgrade del chart

### De Interna a Externa

1. Configurar base de datos externa
2. Migrar datos si es necesario
3. Configurar External Secrets
4. Cambiar `db.enabled: false`
5. Cambiar `secret.db.enabled: true`
6. Realizar upgrade del chart

## Troubleshooting

### Verificar Conectividad

```bash
# Test pod para verificar conectividad a DB
kubectl run db-test --rm -i --tty --image postgres:15-alpine -- bash
# Dentro del pod:
pg_isready -h <DB_HOST> -p <DB_PORT> -U <DB_USER>
```

### Ver Logs de Conexión

```bash
kubectl logs -l app.kubernetes.io/component=auth -f
kubectl logs -l app.kubernetes.io/component=rest -f
```

### Verificar Secrets

```bash
# Para External Secrets
kubectl get externalsecret
kubectl describe externalsecret supabase-db

# Para secrets locales
kubectl get secret supabase-db -o yaml
```
