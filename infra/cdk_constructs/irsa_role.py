from typing import List
from constructs import Construct
from cdktf import TerraformModule


class IrsaRole(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        role_name: str,
        oidc_provider_arn: str,
        oidc_provider_url: str,
        namespace: str,
        service_account_name: str,
        policy_arns: List[str] | None = None,
        attach_load_balancer_controller_policy: bool = False,
    ) -> None:
        super().__init__(scope, id)

        vars = {
            "role_name": role_name,
            "oidc_providers": {
                "main": {
                    "provider_arn": oidc_provider_arn,
                    "provider_url": oidc_provider_url,
                    "namespace_service_accounts": [f"{namespace}:{service_account_name}"],
                }
            },
        }

        if policy_arns:
            vars["role_policy_arns"] = policy_arns
        if attach_load_balancer_controller_policy:
            vars["attach_load_balancer_controller_policy"] = True

        self.module = TerraformModule(
            self,
            "irsa",
            source="terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks",
            version="~> 5.0",
        )
        self.module.add_override("variables", vars)

    @property
    def role_arn(self) -> str:
        return self.module.get_string("iam_role_arn")
