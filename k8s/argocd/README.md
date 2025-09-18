
# ArgoCD Installation

## 🚀 Quick Install (Non-Production)

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## 📋 Setup
1. Run the commands above
2. Configure an application manually in ArgoCD UI
3. ArgoCD will manage all Helm charts automatically

## ⚠️ Important Note
This is a **non-production** installation for exercises and testing. ArgoCD was chosen for practicality when managing Helm charts in this development environment.

## 📚 More Info: https://argo-cd.readthedocs.io/en/stable/getting_started/
