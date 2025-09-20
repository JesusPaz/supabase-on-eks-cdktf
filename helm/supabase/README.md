# Supabase Helm Chart - Production Ready

Customized Helm chart for deploying Supabase on AWS EKS with production-grade configurations.

## What this chart deploys

**Complete Supabase stack:**
- **Auth** (GoTrue) - User authentication and JWT management
- **PostgREST** - Automatic REST API for PostgreSQL
- **Realtime** - WebSocket subscriptions and live updates
- **Storage** - File upload/download with S3 integration
- **Studio** - Web dashboard for database management
- **Kong** - API Gateway and reverse proxy
- **Meta** - PostgreSQL metadata API
- **Functions** - Edge functions runtime
- **Analytics** - Logging and metrics (Logflare)

## Production Features

**External integrations:**
- **Amazon RDS PostgreSQL** - External managed database
- **Amazon S3** - Object storage via IRSA (no API keys)
- **AWS Secrets Manager** - Centralized secret management
- **External Secrets Operator** - Automatic secret synchronization

**Scaling & Performance:**
- **HPA enabled** - Auto-scaling for all services based on CPU
- **Resource limits** - Memory and CPU limits configured
- **Multi-replica** - High availability deployment
- **Health checks** - Liveness and readiness probes

**Security:**
- **NetworkPolicies** - Micro-segmentation with Calico
- **IRSA** - AWS access without hardcoded credentials
- **TLS encryption** - All connections encrypted
- **Private database** - RDS in private subnets only

## Quick deployment

```bash
# Deploy via ArgoCD (GitOps)
kubectl apply -f k8s/supabase/supabase-application.yaml

# Or direct Helm
helm upgrade --install supabase ./helm/supabase \
  --values ./helm/supabase/values.yaml \
  --namespace supabase --create-namespace
```

## Configuration

**Key customizations in `values.yaml`:**
- External RDS connection via secrets
- S3 integration with IRSA
- External Secrets from AWS Secrets Manager
- ALB ingress with SSL termination
- HPA settings for auto-scaling
- NetworkPolicy configurations

**All secrets managed externally** - No hardcoded credentials in chart.
