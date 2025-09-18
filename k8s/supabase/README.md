# Supabase Helm Chart

This directory contains the Supabase Helm chart configuration for deployment on EKS with AWS Secrets Manager integration.

## 🔐 Security Best Practices

This chart uses **External Secrets Operator** to fetch secrets from **AWS Secrets Manager** instead of storing them in Kubernetes secrets. This follows security best practices by:

- ✅ Centralizing secrets in AWS Secrets Manager
- ✅ Using IRSA for secure AWS API access
- ✅ Automatic secret rotation support
- ✅ No secrets stored in Git or Kubernetes manifests

## 📋 Prerequisites

1. **Infrastructure deployed** (EKS cluster, RDS, S3, etc.)
2. **External Secrets Operator** installed
3. **AWS Load Balancer Controller** installed
4. **ArgoCD** installed and configured

## 🚀 Deployment

### Option 1: ArgoCD Application (Recommended)
```bash
kubectl apply -f supabase-application.yaml
```

### Option 2: Direct Helm
```bash
helm repo add supabase https://supabase.github.io/supabase-kubernetes
helm install supabase supabase/supabase -f values.yaml -n supabase --create-namespace
```

## 🔧 Configuration

The chart is configured to:
- Use **AWS RDS PostgreSQL** (external database)
- Use **AWS S3** for storage
- Fetch all secrets from **AWS Secrets Manager**
- Use **AWS Load Balancer** for ingress
- Enable **metrics and monitoring**

## 📁 Files

- `supabase-application.yaml` - ArgoCD application definition
- `values.yaml` - Helm chart values
- `external-secrets/` - Secret store configurations
- `secrets/` - Secret definitions for External Secrets

## 🔗 External Dependencies

This chart requires the following AWS resources (created by Terraform):
- RDS PostgreSQL database
- S3 bucket for storage
- Secrets in AWS Secrets Manager
- IRSA roles for service accounts
