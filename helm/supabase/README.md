# Supabase Helm Chart

Production-ready Supabase deployment for AWS EKS.

## What This Is

**Custom Helm chart based on the [supabase-kubernetes](https://github.com/supabase-community/supabase-kubernetes) community chart** - adapted for production AWS deployment with external RDS and S3.

**What gets deployed:**
- **Auth** - User authentication and JWT management
- **PostgREST** - Automatic REST API for your database
- **Realtime** - WebSocket subscriptions and live updates
- **Storage** - File upload/download with S3 integration
- **Studio** - Web dashboard for managing everything
- **Kong** - API Gateway routing all requests
- **Meta** - PostgreSQL metadata API
- **Analytics** - Logging and metrics

## Production Setup

**External AWS services:**
- **RDS PostgreSQL** - Managed database in private subnets
- **S3 bucket** - File storage with IRSA (no API keys needed)
- **Secrets Manager** - All secrets stored securely
- **External Secrets** - Auto-sync secrets to Kubernetes

**Built for scale:**
- **Auto-scaling** - HPA configured for all services
- **High availability** - Multiple replicas across AZs
- **Health checks** - Proper liveness and readiness probes
- **Resource limits** - CPU and memory limits set

**Security first:**
- **NetworkPolicies** - Control traffic between services
- **IRSA** - Secure AWS access without hardcoded keys
- **Private RDS** - Database never accessible from internet
- **TLS everywhere** - All connections encrypted

## How to Deploy

**Via ArgoCD (recommended):**
```bash
kubectl apply -f k8s/supabase/supabase-application.yaml
```

**Direct Helm install:**
```bash
helm upgrade --install supabase ./helm/supabase \
  --values ./helm/supabase/values.yaml \
  --namespace supabase --create-namespace
```

## Key Differences from Community Chart

**What I changed for production AWS:**
- **External RDS** - Uses AWS RDS instead of in-cluster PostgreSQL
- **S3 integration** - IRSA for secure S3 access without API keys
- **External Secrets** - AWS Secrets Manager integration
- **ALB ingress** - AWS Load Balancer Controller for SSL termination
- **NetworkPolicies** - Calico policies for pod-to-pod security
- **Auto-scaling** - HPA configured for all services

**All secrets come from AWS** - No hardcoded credentials anywhere in the chart.
