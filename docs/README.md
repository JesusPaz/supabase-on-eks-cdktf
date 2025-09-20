# Documentation

Everything you need to know about this Supabase deployment.

## The Complete Guide


1. **[Technology Choices](01-technology-choices.md)** - Why I picked these tools
2. **[Prerequisites & Setup](02-prerequisites-setup.md)** - What you need to get started
3. **[Deployment Instructions](03-deployment-instructions.md)** - How to deploy everything
4. **[Verification Guide](04-verification-guide.md)** - How to check it's working
5. **[Teardown Instructions](05-teardown-instructions.md)** - How to clean up and avoid charges
6. **[Security & Scalability](06-security-scalability.md)** - How I handled security and scaling
7. **[Challenges & Learnings](07-challenges-learnings.md)** - What was hard and what I learned
8. **[Future Improvements](08-future-improvements.md)** - What I'd build next

## Implementation Details

**Code and configs:**
- **[Infrastructure](../infra/README.md)** - CDKTF code for AWS resources
- **[Kubernetes](../k8s/README.md)** - ArgoCD applications and GitOps setup
- **[Helm Chart](../helm/supabase/README.md)** - Supabase configuration and values
- **[Tests](../test/README.md)** - API test suite and validation
- **[Diagrams](../diagrams/README.md)** - Architecture visuals

**Follow the numbered docs in order for the smoothest experience.**
