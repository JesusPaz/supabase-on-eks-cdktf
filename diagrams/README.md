# Architecture Diagrams

Visual overview of the Supabase on AWS EKS deployment.

## Diagrams

### [01-architecture-overview.png](./01-architecture-overview.png)
**High-level AWS infrastructure architecture**
- VPC with public/private subnets across 2 AZs
- EKS cluster with worker nodes in private subnets
- RDS PostgreSQL Multi-AZ with encryption
- S3 storage with versioning and encryption
- ALB for external access, NAT for egress
- KMS keys for encryption, Secrets Manager for credentials

### [02-security-network-diagram.png](./02-security-network-diagram.png)
**Security and network architecture**
- Network segmentation with security groups
- Calico NetworkPolicies for pod-to-pod restrictions
- IRSA for AWS access without API keys
- TLS encryption for all connections
- IAM roles with least privilege access
- Audit logging and compliance controls

### [03-data-flow-interactions.png](./03-data-flow-interactions.png)
**Data flow and service interactions**
- User traffic: Browser/API → ALB → Kong → Services
- Database operations: Services → RDS PostgreSQL
- File operations: Storage service → S3 bucket
- Real-time data: WebSocket connections via Realtime
- Secret management: External Secrets → AWS Secrets Manager
- GitOps deployment: ArgoCD → Kubernetes resources
