# Supabase ArgoCD Application

ArgoCD Application for deploying complete Supabase stack with full functionality.

## Complete Supabase Stack

**All services included and functional:**
- Auth, PostgREST, Realtime, Storage, Studio, Kong, Meta, Functions, Analytics
- External RDS PostgreSQL integration
- S3 storage with IRSA (no API keys)
- External Secrets from AWS Secrets Manager
- HPA auto-scaling enabled
- NetworkPolicies for micro-segmentation

## Deployment

**GitOps deployment via ArgoCD:**
```bash
kubectl apply -f supabase-application.yaml
```

**Direct Helm deployment:**
```bash
helm upgrade --install supabase ../../helm/supabase \
  --values ../../helm/supabase/values.yaml \
  --namespace supabase --create-namespace
```

## Configuration

**Production-ready features:**
- External RDS PostgreSQL (Multi-AZ, encrypted)
- S3 integration via IRSA (secure, no hardcoded keys)
- AWS Secrets Manager for all credentials
- ALB ingress with SSL termination
- Horizontal Pod Autoscaler on all services
- Calico NetworkPolicies for security

**References:**
- Full Helm chart: [../../helm/supabase/](../../helm/supabase/)
- Complete test suite: [../../test/](../../test/)

**All secrets sourced from AWS** - No credentials in Git or Kubernetes manifests.
