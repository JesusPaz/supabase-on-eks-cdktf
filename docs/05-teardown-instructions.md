# Teardown Guide

How to clean up everything and avoid AWS charges.

## Step 1: Remove Kubernetes Stuff

**Clean up the cluster first:**

```bash
# Remove Supabase from ArgoCD
kubectl delete application supabase -n argocd

# Clean up other applications
kubectl delete -f k8s/external-secrets/
kubectl delete -f k8s/networking/

# Remove ArgoCD itself
kubectl delete namespace argocd
```

## Step 2: Destroy AWS Infrastructure

**This removes everything:**

```bash
cd infra/
make destroy

# Takes about 10-15 minutes
# Watch for any errors and handle them
```

## Step 3: Double-Check Everything's Gone

**Make sure nothing's left running:**

```bash
# Should return empty
aws eks list-clusters --query 'clusters[?contains(@, `supabase`)]'
aws rds describe-db-instances --query 'DBInstances[?contains(DBInstanceIdentifier, `supabase`)]'
```

## If Something Gets Stuck

**Sometimes AWS resources don't delete cleanly:**

```bash
# Check for leftover S3 buckets
aws s3 ls | grep supabase

# Force delete if needed
aws s3 rm s3://BUCKET_NAME --recursive
aws s3 rb s3://BUCKET_NAME

# Check for stuck load balancers
aws elbv2 describe-load-balancers --query 'LoadBalancers[?contains(LoadBalancerName, `k8s`)]'
```

**That's it** - everything should be cleaned up and you won't get charged for anything.
