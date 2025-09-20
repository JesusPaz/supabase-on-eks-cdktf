# Technology Choices

## Main Decisions

| **Component** | **Choice** | **Why** |
|---------------|------------|---------|
| **IaC Framework** | CDKTF (Python) | Familiar syntax, type safety |
| **Cloud Provider** | AWS | IRSA, mature EKS ecosystem |
| **Database** | RDS PostgreSQL + Lambda | Cost savings vs Aurora |
| **Secrets** | AWS Secrets Manager | Keep everything in AWS |
| **GitOps** | ArgoCD | Personal experience, easy Helm management |
| **Networking** | Calico NetworkPolicies | Better than basic policies |

## Why These Choices

### CDKTF (Python)
**Required by the assignment** - The take-home task specifically asked for CDKTF. I'm more of a Terraform HCL person usually, but I know Python and didn't mind using it. Turned out to be a different and interesting way to create infrastructure. I liked it and would use it again.

### AWS Ecosystem
**Kept everything in one cloud** - IRSA eliminates the need for API keys in pods, which is a huge security win. EKS is mature and integrates well with other AWS services.

### RDS vs Aurora
**Cost consideration** - RDS is about 50% cheaper than Aurora. Aurora has better features (serverless scaling, better point-in-time recovery), but for this use case, RDS with a custom Lambda migration setup works fine and saves money.

### AWS Secrets Manager
**Simplicity over complexity** - Could have used git-crypt, but losing GPG keys means losing access to all secrets. Other cloud providers would add multi-cloud complexity. AWS Secrets Manager keeps everything in one ecosystem and External Secrets makes it easy to sync to Kubernetes.

### ArgoCD
**Personal preference** - I've used ArgoCD before, so it's faster for me to set up and troubleshoot. It handles Helm charts better than doing manual kubectl or Terraform, and having all deployments versioned in one place is convenient.

### Calico NetworkPolicies
**Better than basic** - Calico's policy-only mode works well with AWS VPC CNI and provides more advanced features than standard Kubernetes NetworkPolicies.

## Migration Strategy

**Lambda approach** - Built a custom Lambda function to handle all database migrations. This was inspired by the [supabase-on-aws](https://github.com/supabase-community/supabase-on-aws) community implementation. Lambda connects to the private RDS instance and runs all the SQL scripts needed to set up Supabase (extensions, users, schemas, etc.).

**Why Lambda:** Easier than trying to run migrations from Kubernetes pods, and it's idempotent so you can run it multiple times safely.
