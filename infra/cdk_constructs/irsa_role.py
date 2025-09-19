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
        attach_ebs_csi_policy: bool = False,
        attach_cluster_autoscaler_policy: bool = False,
    ) -> None:
        super().__init__(scope, id)

        self.module = TerraformModule(
            self,
            "irsa",
            source="terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts"
        )
        
        self.module.add_override("name", role_name)
        self.module.add_override("oidc_providers", {
            "main": {
                "provider_arn": oidc_provider_arn,
                "namespace_service_accounts": [f"{namespace}:{service_account_name}"],
            }
        })
        
        if policy_arns:
            self.module.add_override("policies", {f"policy_{i}": arn for i, arn in enumerate(policy_arns)})
        if attach_load_balancer_controller_policy:
            self.module.add_override("attach_load_balancer_controller_policy", True)
        if attach_ebs_csi_policy:
            self.module.add_override("attach_ebs_csi_policy", True)
        if attach_cluster_autoscaler_policy:
            self.module.add_override("attach_cluster_autoscaler_policy", True)

    @property
    def role_arn(self) -> str:
        return self.module.get_string("arn")
