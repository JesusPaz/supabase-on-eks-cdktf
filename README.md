# Supabase on AWS EKS - Production Deployment

Complete production-ready Supabase deployment on AWS EKS using CDKTF, Helm, and GitOps.

## Overview

**Full-stack implementation featuring:**
- AWS infrastructure via CDKTF (VPC, EKS, RDS, S3, Secrets Manager)
- Complete Supabase deployment with all services functional
- GitOps automation with ArgoCD
- Comprehensive security with NetworkPolicies and IRSA
- Production-grade testing and validation

## Architecture

See [Architecture Diagrams](diagrams/) for visual overview:
- [Infrastructure Overview](diagrams/01-architecture-overview.png)
- [Security & Network](diagrams/02-security-network-diagram.png)  
- [Data Flow](diagrams/03-data-flow-interactions.png)

## Documentation

| **Topic** | **Documentation** |
|-----------|-------------------|
| **Infrastructure** | [infra/README.md](infra/README.md) |
| **Kubernetes Apps** | [k8s/README.md](k8s/README.md) |
| **Helm Chart** | [helm/supabase/README.md](helm/supabase/README.md) |
| **API Testing** | [test/README.md](test/README.md) |
| **Architecture** | [diagrams/README.md](diagrams/README.md) |
| **Detailed Guides** | [docs/](docs/) |

## Key Features

**Security:** Private subnets, IRSA, External Secrets, NetworkPolicies, encryption everywhere
**Scalability:** HPA auto-scaling, cluster autoscaler, Multi-AZ deployment
**Automation:** GitOps with ArgoCD, automated testing, Infrastructure as Code
**Production-ready:** External RDS, S3 integration, comprehensive monitoring

## Status

✅ **Infrastructure** - AWS resources deployed and functional
✅ **Applications** - All Supabase services running  
✅ **Security** - NetworkPolicies and encryption enabled
✅ **Testing** - 13/14 API tests passing (93% success rate)
✅ **GitOps** - ArgoCD managing deployments

**Live instance:** https://supabase.stack-ai.jesuspaz.com