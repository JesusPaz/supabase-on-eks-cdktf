
# ArgoCD - GitOps Controller

GitOps controller for automated Kubernetes application deployment from Git repositories.

## Purpose

**ArgoCD** enables GitOps by:
- Monitoring GitHub repository for changes
- Automatically deploying applications when code changes
- Ensuring cluster state matches Git repository state
- Providing rollback and audit capabilities

## Installation

**Bootstrap deployment** (manual one-time setup):

```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## Access

**Option 1: External access (Production)**
```bash
# Access via ALB ingress
https://argocd.stack-ai.jesuspaz.com
```

**Option 2: Local access (Development)**
```bash
# Port forward for local access
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Then open: http://localhost:8080
```

## Configuration

**After installation, ArgoCD manages all other applications:**
- External Secrets Operator
- Metrics Server
- Cluster Autoscaler  
- AWS Load Balancer Controller
- Calico NetworkPolicies
- Supabase application stack

## GitOps Workflow

```bash
# 1. Make changes to k8s/ manifests
# 2. Push to GitHub
git push origin main

# 3. ArgoCD detects changes automatically
# 4. Applications are deployed/updated
# 5. Monitor via ArgoCD UI at localhost:8080
```

## Benefits

**Automated deployment:**
- No manual kubectl/helm commands after setup
- Consistent deployments across environments
- Git-based audit trail of all changes

**Operational efficiency:**
- Visual diff of changes before deployment
- Easy rollback to previous Git commits
- Centralized application management

**Note:** This is the only component requiring manual installation - all others deploy via GitOps.
