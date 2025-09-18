
# ArgoCD Installation

## 🚀 Quick Install (Non-Production)

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## 📋 Setup
1. Run the commands above
2. Access ArgoCD UI:
   ```bash
   kubectl port-forward svc/argocd-server -n argocd 8080:443
   ```
   Then open: http://localhost:8080
3. Configure an application manually in ArgoCD UI
4. ArgoCD will manage all Helm charts automatically

## ⚠️ Important Note
This is a **non-production** installation for exercises and testing. ArgoCD was chosen for practicality when managing Helm charts in this development environment.

## 📚 More Info: https://argo-cd.readthedocs.io/en/stable/getting_started/
