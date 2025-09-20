# Deployment Guide

How to deploy everything from scratch.

## Step 1: Deploy AWS Infrastructure

```bash
cd infra/

# Set up the environment
make bootstrap

# See what will be created
make synth
make plan

# Deploy everything to AWS
make deploy
```

**This creates:** VPC, EKS cluster, RDS database, S3 bucket, secrets, and IAM roles. Takes about 15-20 minutes.

## Step 2: Connect to Kubernetes

```bash
# Connect kubectl to your new EKS cluster
aws eks update-kubeconfig --name supabase-on-eks --profile personal

# Make sure it worked
kubectl get nodes
```

**Note about EKS API access:** For this exercise, I left the Kubernetes API endpoint public to make testing easier. **In production, this should definitely be private** for security. I know this isn't a production best practice, but I did it this way to avoid setting up a VPN or bastion host just for this demo. In a real production environment, you'd want:
- Private EKS API endpoint
- VPN or bastion host for kubectl access
- No direct internet access to the Kubernetes API

## Step 3: Set Up ArgoCD

```bash
# Install ArgoCD (this is the only manual step)
kubectl apply -f k8s/argocd/

# Wait for it to start up
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd
```

## Step 4: Configure ArgoCD Applications

**After ArgoCD is installed, you need to configure it to watch this GitHub repository.**

Follow the official guide: [ArgoCD Getting Started](https://argo-cd.readthedocs.io/en/stable/getting_started/)

**Key steps:**
1. Access ArgoCD UI (port-forward or ingress)
2. Login with admin credentials
3. Add this GitHub repository: `https://github.com/JesusPaz/supabase-on-eks-cdktf`
4. Configure applications to watch the `k8s/` directory

**I didn't include the detailed steps here** since the official ArgoCD documentation explains it better with screenshots and step-by-step instructions.

## Step 5: GitOps Magic

**Once ArgoCD is configured, you don't need kubectl apply anymore:**

```bash
# Make changes to any files in k8s/
# Push to GitHub
git push origin main

# ArgoCD detects changes and deploys automatically
# Watch it happen in the ArgoCD UI
```

**That's the beauty of GitOps** - after initial setup, deployments happen automatically when you push to the main branch.

## Timeline & Safety

**Whole process takes about 30-45 minutes** - most of that is AWS spinning up resources. The actual commands are pretty quick.

**Everything is idempotent** - you can run all commands multiple times safely:
- `make deploy` won't break existing infrastructure
- `kubectl apply` updates existing resources
- ArgoCD handles application updates gracefully

## If Something Goes Wrong

```bash
# Check what ArgoCD is doing
kubectl get applications -n argocd

# Look at pod logs
kubectl logs -n supabase -l app.kubernetes.io/name=supabase-auth

# Re-run deployment (it's safe)
make deploy
```

**Access the dashboard:** https://supabase.stack-ai.jesuspaz.com

**For testing and verification, see the next document.**
