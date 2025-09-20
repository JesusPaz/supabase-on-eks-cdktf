# Infrastructure as Code - CDKTF

Production-ready AWS infrastructure for Supabase on EKS using CDK for Terraform (Python).

## What this deploys

**AWS Infrastructure:**
- **VPC** - Multi-AZ with public/private subnets, NAT Gateway
- **EKS** - Managed Kubernetes cluster with IRSA enabled
- **RDS** - PostgreSQL Multi-AZ with encryption and automated backups
- **S3** - Object storage with versioning and encryption
- **Secrets Manager** - Centralized secret storage with rotation
- **KMS** - Encryption keys for all services
- **IAM** - Least privilege roles for External Secrets and IRSA
- **Lambda** - Database migration functions with VPC access

## Key Features

**Security:**
- Private subnets for all workloads
- Encryption at rest and in transit (KMS)
- Managed secrets (no hardcoded credentials)
- VPC endpoints to reduce NAT egress

**High Availability:**
- Multi-AZ deployment across 2 availability zones
- RDS Multi-AZ with automated failover
- EKS worker nodes distributed across AZs
- Automated backups and point-in-time recovery

**Automation:**
- Database migrations via Lambda functions
- Secret rotation capabilities
- Infrastructure as Code (no manual configuration)

## Architecture

See detailed architecture diagrams:
- [Architecture Overview](../diagrams/01-architecture-overview.png) - Complete AWS infrastructure
- [Security Diagram](../diagrams/02-security-network-diagram.png) - Security controls and network isolation
- [Data Flow](../diagrams/03-data-flow-interactions.png) - Service interactions and data paths

## Deployment

```bash
# Install dependencies and setup
make bootstrap

# Generate Terraform code
make synth

# Review changes (optional)
make plan

# Deploy infrastructure
make deploy

# Destroy infrastructure (cleanup)
make destroy
```

## Components

| **Component** | **Purpose** | **File** |
|---------------|-------------|----------|
| **Network** | VPC, subnets, routing | `stacks/network.py` |
| **EKS** | Kubernetes cluster | `stacks/eks.py` |
| **RDS** | PostgreSQL database | `stacks/rds.py` |
| **S3** | Object storage | `stacks/s3.py` |
| **Secrets** | Secret management | `stacks/secrets.py` |
| **IAM** | Roles and policies | `stacks/iam.py` |
| **KMS** | Encryption keys | `stacks/kms.py` |
| **Migrations** | Database setup | `stacks/db_migrations.py` |

## Outputs

After deployment, use these outputs for Kubernetes configuration:
- `cluster_name` - EKS cluster name for kubectl
- `db_master_user_secret_arn` - RDS credentials for External Secrets
- `s3_bucket_name` - Storage bucket for Supabase
- `irsa_role_arns` - IAM roles for service accounts

**Next step:** Deploy Supabase using [Helm chart](../helm/supabase/)
