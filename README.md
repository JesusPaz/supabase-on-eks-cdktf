# Supabase on EKS with CDKTF (Infra only)

Minimal, production-ready AWS infra for running Supabase on EKS using CDK for Terraform (Python). No Helm/manifests yet.

## What you get
- Private VPC (public+private subnets, NAT, DNS)
- EKS (private endpoint, IRSA enabled, 1 managed node group)
- RDS PostgreSQL (Multi-AZ, encrypted, backups, master password in Secrets Manager)
- S3 storage (public access blocked, versioning, encryption, SSL-only)
- IAM roles for ALB Controller, External Secrets, and app S3 access
- App secrets placeholders in Secrets Manager (JWT, anon, service)

## Minimal production-ready settings applied
- RDS master password managed by AWS Secrets Manager (no plaintext in code/outputs)
- RDS Multi-AZ, encryption at rest, 7-day backups
- S3: BPA, versioning, SSE (AES256), SSL-only policy, ownership controls
- EKS: private-only endpoint, IRSA enabled
- IAM: least-privilege for ESO (read supabase/*) and app S3 (bucket vs object actions)

## Next hardening steps (recommended)
- EKS control-plane logs + KMS envelope encryption for K8s secrets
- NAT per AZ, VPC Flow Logs, VPC endpoints (S3, SecretsManager, ECR, STS, CWL)
- RDS: deletion protection + final snapshot, CW logs exports, Performance Insights (KMS), SSL-only param group
- S3: SSE-KMS key, access logging to dedicated log bucket, lifecycle rules
- Terraform backend: S3 + DynamoDB lock, workspaces per environment
- Kubernetes: NetworkPolicies, Ingress/ALB Controller, External Secrets CRDs

## Usage
- Prereq: `npm i -g cdktf-cli`, AWS creds set.
- Bootstrap: `make bootstrap`
- Synth: `make synth`
- Deploy: `make deploy`
- Destroy: `make destroy`

Notes: Real secret values should be set via Secrets Manager or CI/CD, not in code. When adding Helm/manifests, read DB creds from the `db_master_user_secret_arn` output.