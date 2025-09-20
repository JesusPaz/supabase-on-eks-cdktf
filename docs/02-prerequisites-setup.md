# Prerequisites & Setup

## What You'll Need

### Tools to Install
```bash
# Basic tools for the deployment
npm install -g cdktf-cli
brew install kubectl helm jq
```

### AWS Setup
```bash
# Configure your AWS credentials
aws configure --profile personal
export AWS_PROFILE=personal

# Make sure it works
aws sts get-caller-identity
```

### Domain Configuration
**I used my own domain** - `stack-ai.jesuspaz.com` with an SSL certificate from ACM. You'll need:
- A domain configured in Route53
- An ACM certificate for `*.your-domain.com`
- Update the certificate ARN in the ingress manifests

## What Gets Created Automatically

**No manual configuration needed for:**
- RDS master password (AWS generates it)
- S3 bucket names (Terraform creates them)
- JWT tokens (stored in AWS Secrets Manager)
- Kubernetes secrets (External Secrets syncs them)

**You just need AWS credentials and a domain** - everything else is automated.
