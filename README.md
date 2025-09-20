# Supabase on AWS EKS

Production-ready Supabase running on AWS with everything you need.

## What This Is

**A complete Supabase deployment that actually works:**
- AWS infrastructure built with CDKTF (VPC, EKS, RDS, S3, secrets)
- All Supabase services running and functional
- GitOps with ArgoCD for easy management
- Proper security with NetworkPolicies and IRSA
- Real API tests to prove it works

## Quick Start

**Deploy everything:**
```bash
# 1. Set up infrastructure
cd infra && make bootstrap && make deploy

# 2. Deploy applications
kubectl apply -f k8s/argocd/
kubectl apply -f k8s/external-secrets/
kubectl apply -f k8s/supabase/

# 3. Test it works
cd test && make all
```

**Live demo:** https://supabase.stack-ai.jesuspaz.com

## Architecture

**Visual overview:**
- **[Infrastructure](diagrams/01-architecture-overview.png)** - AWS resources and connections
- **[Security](diagrams/02-security-network-diagram.png)** - Network and access control
- **[Data Flow](diagrams/03-data-flow-interactions.png)** - How requests flow through services

## Documentation

**Implementation details:**
- **[Infrastructure](infra/README.md)** - CDKTF code for AWS resources
- **[Kubernetes](k8s/README.md)** - ArgoCD applications and GitOps
- **[Helm Chart](helm/supabase/README.md)** - Supabase configuration
- **[Tests](test/README.md)** - API validation suite
- **[Complete Guide](docs/)** - Step-by-step instructions

## What's Working

✅ **Infrastructure** - All AWS resources deployed and running
✅ **Supabase services** - Auth, PostgREST, Storage, Realtime functional  
✅ **Security** - Private RDS, NetworkPolicies, IRSA, encrypted secrets
✅ **Auto-scaling** - HPA and cluster autoscaler configured
✅ **GitOps** - ArgoCD managing all deployments
✅ **Testing** - 13/14 API tests passing (93% success rate)

## Key Features

**Security first:**
- Private subnets and RDS (no internet access)
- IRSA for secure AWS access (no hardcoded keys)
- External Secrets for centralized secret management
- NetworkPolicies for pod-to-pod security
- Encryption everywhere (TLS, KMS, RDS)

**Production ready:**
- External RDS with Multi-AZ and backups
- S3 integration with proper IAM roles
- HPA auto-scaling based on CPU usage
- Cluster autoscaler for node management
- Comprehensive API testing suite

**Easy to manage:**
- GitOps with ArgoCD for deployments
- Infrastructure as Code with CDKTF
- Automated testing and validation
- Clear documentation and guides