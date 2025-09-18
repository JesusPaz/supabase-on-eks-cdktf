from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from cdktf_cdktf_provider_aws.provider import AwsProvider

# Stacks / Constructs
from stacks.network import Network
from stacks.eks import Eks
from stacks.rds import Rds
from stacks.s3 import StorageBucket
from stacks.iam import IamRoles
from stacks.secrets import Secrets
from stacks.vpc_endpoints import VpcEndpoints
from stacks.eks_addons import EksAddons
from cdk_constructs.common_tags import CommonTags
from stacks.kms import KmsStack


class InfraStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        region = "us-east-1"
        project = "supabase-on-eks"
        environment = "prod"

        AwsProvider(self, "aws", region=region)

        # Common tags
        common = CommonTags(self, "tags", project=project, environment=environment, owner="platform", cost_center="eng"); tags = common.tags

        # Networking (VPC, subnets, routing)
        network = Network(self, "network", vpc_name=f"{project}-vpc", tags=tags)

        # KMS Keys for S3 and EKS secrets encryption
        kms = KmsStack(self, "kms", project=project, environment=environment, tags=tags)

        # EKS cluster in private subnets with IRSA enabled and control plane logs
        eks = Eks(
            self,
            "eks",
            cluster_name=f"{project}",
            vpc_id=network.vpc_id,
            private_subnet_ids=network.private_subnet_ids,
            public_subnet_ids=network.public_subnet_ids,
            kms_key_arn_for_secrets=kms.eks_key_arn,
            tags=tags,
        )

        # EKS managed addons
        EksAddons(self, "addons", cluster_name=eks.cluster_name, tags=tags)

        # VPC Endpoints to reduce NAT/egress needs
        VpcEndpoints(
            self,
            "vpce",
            vpc_id=network.vpc_id,
            private_subnet_ids=network.private_subnet_ids,
            private_route_table_ids=network.private_route_table_ids,
            region=region,
            security_group_ids=[eks.node_security_group_id],
            tags=tags,
        )

        # RDS PostgreSQL in private subnets secured to EKS nodes
        rds = Rds(
            self,
            "rds",
            db_name="supabase",
            vpc_id=network.vpc_id,
            private_subnet_ids=network.private_subnet_ids,
            eks_node_sg_id=eks.node_security_group_id,
        )

        # S3 bucket for Supabase storage with KMS
        bucket = StorageBucket(self, "storage", bucket_prefix=f"{project}-storage-", use_kms=True, kms_key_arn=kms.s3_key_arn, tags=tags)

        # IAM roles and IRSA bindings (ALB Controller, External Secrets, App S3)
        IamRoles(
            self,
            "iam",
            oidc_provider_arn=eks.oidc_provider_arn,
            oidc_provider_url=eks.oidc_provider_url,
            cluster_name=eks.cluster_name,
            bucket_arn=bucket.bucket_arn,
            bucket_name=bucket.bucket_name,
        )

        # App-level secrets placeholders (JWT, anon, service role)
        Secrets(self, "secrets")

        # Outputs
        TerraformOutput(self, "s3_bucket_name", value=bucket.bucket_name)
        TerraformOutput(self, "s3_bucket_arn", value=bucket.bucket_arn)
        TerraformOutput(self, "db_endpoint", value=rds.db_endpoint)
        TerraformOutput(self, "db_name", value=rds.db_name)
        TerraformOutput(self, "db_master_user_secret_arn", value=rds.master_user_secret_arn)
        TerraformOutput(self, "cluster_name", value=eks.cluster_name)
        TerraformOutput(self, "kubeconfig_path", value=eks.kubeconfig_path)


app = App()
InfraStack(app, "supabase-on-eks")
app.synth()
