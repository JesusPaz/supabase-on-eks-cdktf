from constructs import Construct
from cdktf import TerraformModule
from cdk_constructs.irsa_role import IrsaRole


class IamRoles(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        oidc_provider_arn: str,
        oidc_provider_url: str,
        cluster_name: str,
        bucket_arn: str,
        bucket_name: str,
    ) -> None:
        super().__init__(scope, id)

        self.alb_controller = IrsaRole(
            self,
            "alb_controller",
            role_name=f"{cluster_name}-alb-controller",
            oidc_provider_arn=oidc_provider_arn,
            oidc_provider_url=oidc_provider_url,
            namespace="kube-system",
            service_account_name="aws-load-balancer-controller",
            attach_load_balancer_controller_policy=True,
        )

        eso_policy = TerraformModule(
            self,
            "eso_secrets_ro_policy",
            source="terraform-aws-modules/iam/aws//modules/iam-policy",
            version="~> 5.0",
        )
        eso_policy.add_override("name", f"{cluster_name}-eso-secrets-ro")
        eso_policy.add_override("path", "/")
        eso_policy.add_override(
            "policy",
            '{\n'
            '  "Version": "2012-10-17",\n'
            '  "Statement": [\n'
            '    {\n'
            '      "Effect": "Allow",\n'
            '      "Action": ["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"],\n'
            '      "Resource": ["arn:aws:secretsmanager:*:*:secret:supabase/*"]\n'
            '    },\n'
            '    {\n'
            '      "Effect": "Allow",\n'
            '      "Action": ["secretsmanager:ListSecrets"],\n'
            '      "Resource": "*"\n'
            '    }\n'
            '  ]\n'
            '}',
        )

        self.external_secrets = IrsaRole(
            self,
            "external_secrets",
            role_name=f"{cluster_name}-external-secrets",
            oidc_provider_arn=oidc_provider_arn,
            oidc_provider_url=oidc_provider_url,
            namespace="external-secrets",
            service_account_name="external-secrets",
            policy_arns=[eso_policy.get_string("arn")],
        )

        s3_policy = TerraformModule(
            self,
            "app_s3_policy",
            source="terraform-aws-modules/iam/aws//modules/iam-policy",
            version="~> 5.0",
        )
        s3_policy.add_override("name", f"{cluster_name}-app-s3-access")
        s3_policy.add_override("path", "/")
        s3_policy.add_override(
            "policy",
            '{\n'
            '  "Version": "2012-10-17",\n'
            '  "Statement": [\n'
            '    {\n'
            '      "Effect": "Allow",\n'
            f'      "Action": ["s3:PutObject","s3:GetObject","s3:DeleteObject","s3:ListBucket"],\n'
            f'      "Resource": ["{bucket_arn}", "{bucket_arn}/*"]\n'
            '    }\n'
            '  ]\n'
            '}',
        )

        self.app_role = IrsaRole(
            self,
            "app_role",
            role_name=f"{cluster_name}-app-s3",
            oidc_provider_arn=oidc_provider_arn,
            oidc_provider_url=oidc_provider_url,
            namespace="supabase",
            service_account_name="supabase-app",
            policy_arns=[s3_policy.get_string("arn")],
        )
