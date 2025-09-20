# Documentation Index

Comprehensive documentation for the Supabase on AWS EKS deployment.

## Documents

| **Document** | **Purpose** |
|--------------|-------------|
| [Technology Choices](01-technology-choices.md) | Justification for CDKTF, AWS, EKS, and other technology decisions |
| [Prerequisites & Setup](02-prerequisites-setup.md) | Required tools, AWS configuration, and initial setup |
| [Deployment Instructions](03-deployment-instructions.md) | Step-by-step deployment guide with timelines |
| [Verification Guide](04-verification-guide.md) | Testing, monitoring, and validation procedures |
| [Teardown Instructions](05-teardown-instructions.md) | Complete cleanup to avoid ongoing costs |
| [Security & Scalability](06-security-scalability.md) | Deep dive into security and scaling architecture |
| [Challenges & Learnings](07-challenges-learnings.md) | Technical challenges and solutions implemented |
| [Future Improvements](08-future-improvements.md) | Roadmap for enhancements and next steps |

## Quick Reference

**For implementation details:**
- [Infrastructure Code](../infra/README.md) - CDKTF components
- [Kubernetes Apps](../k8s/README.md) - GitOps applications  
- [Helm Chart](../helm/supabase/README.md) - Supabase configuration
- [Test Suite](../test/README.md) - API validation
- [Architecture](../diagrams/README.md) - Visual diagrams
