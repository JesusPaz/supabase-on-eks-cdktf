# Supabase on AWS EKS with External Secrets

Esta configuración personalizada del chart de Supabase está optimizada para AWS EKS con:
- External RDS PostgreSQL
- External S3 Storage con IRSA
- AWS Secrets Manager integration via External Secrets Operator
- Application Load Balancer (ALB) Ingress
- Horizontal Pod Autoscaler (HPA) configurado

## Prerequisitos

1. **AWS EKS cluster** con:
   - AWS Load Balancer Controller
   - External Secrets Operator
   - Cluster Autoscaler (opcional)
   - EBS CSI Driver

2. **AWS Resources**:
   - RDS PostgreSQL database
   - S3 bucket para storage
   - AWS Secrets Manager secrets
   - ACM Certificate para HTTPS
   - IRSA roles configurados

3. **ArgoCD** instalado en el cluster

## Estructura de Archivos

```
helm/supabase/
├── Chart.yaml                     # Chart metadata
├── values.yaml                    # Default values (original)
├── values-aws.yaml                # AWS-specific configuration
├── README-AWS.md                  # Este archivo
└── templates/
    ├── external-secrets.yaml      # External Secrets para AWS Secrets Manager
    └── hpa.yaml                   # Horizontal Pod Autoscalers
```

## Configuración de Secrets en AWS Secrets Manager

Los siguientes secrets deben estar creados en AWS Secrets Manager:

### `supabase/jwt`
```json
{
  "secret": "your-jwt-secret-32-chars-min",
  "anon_key": "your-anon-jwt-key",
  "service_role_key": "your-service-role-jwt-key"
}
```

### `supabase/database`
```json
{
  "username": "supabase",
  "password": "your-db-password",
  "database": "supabase",
  "host": "your-rds-endpoint.region.rds.amazonaws.com"
}
```

### `supabase/analytics`
```json
{
  "logflare_api_key": "your-logflare-api-key"
}
```

### `supabase/dashboard`
```json
{
  "username": "supabase",
  "password": "your-dashboard-password"
}
```

### `supabase/s3`
```json
{
  "bucket_name": "your-s3-bucket-name",
  "region": "us-east-1",
  "access_key_id": "NOT_USED_WITH_IRSA",
  "secret_access_key": "NOT_USED_WITH_IRSA"
}
```

## Deployment con ArgoCD

1. **Aplicar la configuración de ArgoCD**:
   ```bash
   kubectl apply -f k8s/supabase/supabase-application.yaml
   ```

2. **Verificar el estado de la aplicación**:
   ```bash
   kubectl get application supabase -n argocd
   ```

3. **Ver los pods de Supabase**:
   ```bash
   kubectl get pods -n supabase
   ```

## Servicios Configurados

- **Studio**: Dashboard web de Supabase
- **Auth**: Servicio de autenticación (GoTrue)
- **REST**: API REST (PostgREST)
- **Realtime**: Subscripciones en tiempo real
- **Storage**: Almacenamiento de archivos (S3)
- **Meta**: API de metadata de PostgreSQL
- **Analytics**: Logs y analytics (Logflare)
- **Functions**: Edge Functions (Deno runtime)
- **Kong**: API Gateway
- **Imgproxy**: Procesamiento de imágenes
- **Vector**: Log collection

## Autoscaling

Todos los servicios principales tienen HPA configurado:
- **Auth**: 2-10 replicas (70% CPU)
- **REST**: 2-15 replicas (70% CPU)
- **Realtime**: 2-8 replicas (70% CPU)
- **Storage**: 2-6 replicas (70% CPU)
- **Kong**: 2-5 replicas (70% CPU)

## Ingress

El servicio está expuesto a través de ALB Ingress en:
- **URL**: https://supabase.stack-ai.jesuspaz.com
- **Certificate**: ACM certificate configurado
- **Subnets**: Public subnets especificadas

## Troubleshooting

1. **Verificar External Secrets**:
   ```bash
   kubectl get externalsecrets -n supabase
   kubectl get secrets -n supabase
   ```

2. **Verificar logs de init containers**:
   ```bash
   kubectl logs <pod-name> -n supabase -c init-db
   ```

3. **Verificar configuración de IRSA**:
   ```bash
   kubectl describe serviceaccount supabase-storage -n supabase
   ```

4. **Verificar ALB Ingress**:
   ```bash
   kubectl get ingress -n supabase
   kubectl describe ingress <ingress-name> -n supabase
   ```

## Personalización

Para modificar la configuración:
1. Editar `values-aws.yaml`
2. Hacer commit y push al repositorio
3. ArgoCD sincronizará automáticamente los cambios

## Monitoreo

Los HPA están configurados para escalar basado en CPU. Para monitoreo adicional:
- Verificar métricas con `kubectl top pods -n supabase`
- Usar ArgoCD UI para ver el estado de la aplicación
- Revisar logs de ALB Controller para problemas de ingress
