# Helm Charts

Kubernetes application charts for deployment.

## Available Charts

| **Chart** | **Description** |
|-----------|-----------------|
| [supabase/](supabase/) | Complete Supabase stack with AWS integrations |

## Usage

```bash
# Deploy Supabase chart
helm upgrade --install supabase ./supabase \
  --values ./supabase/values.yaml \
  --namespace supabase --create-namespace
```

**Note:** Charts are designed for AWS EKS with External Secrets integration.
