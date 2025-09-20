# Kubernetes Applications - GitOps

ArgoCD monitors this entire `k8s/` directory and automatically applies any YAML files or ArgoCD Applications.

## How it works

**ArgoCD watches this repository and handles two types of files:**
- **ArgoCD Applications** → Deploys Helm charts from Git
- **Kubernetes YAML** (regular `.yaml`) → Runs `kubectl apply`
- **Auto-sync** → Detects changes and deploys automatically

## Applications

| **Directory** | **Purpose** | **Type** |
|---------------|-------------|----------|
| **argocd/** | GitOps controller | Manual install ([see instructions](argocd/README.md)) |
| **external-secrets/** | AWS Secrets Manager sync | ArgoCD Application |
| **metrics-server/** | HPA metrics collection | ArgoCD Application |
| **cluster-autoscaler/** | Node auto-scaling | ArgoCD Application |
| **networking/** | ALB Controller, Calico, NetworkPolicies | ArgoCD Application + K8s YAML |
| **supabase/** | Complete Supabase stack | ArgoCD Application (Helm chart) |

## Deployment

### 1. Install ArgoCD
See [argocd/README.md](argocd/README.md) for manual installation instructions.

### 2. ArgoCD will detect and deploy everything automatically

## GitOps Benefits

- **Automated** - Push to GitHub triggers deployments
- **Declarative** - Git is source of truth
- **Auditable** - Full change history in Git
- **Rollback** - Easy revert to previous versions

**After ArgoCD installation, all deployments are automated via Git.**
