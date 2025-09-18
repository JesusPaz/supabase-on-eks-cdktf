from typing import List, Optional
from constructs import Construct
from cdktf import TerraformModule


class Eks(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        cluster_name: str,
        vpc_id: str,
        private_subnet_ids: List[str],
        public_subnet_ids: List[str] | None = None,
        cluster_version: str = "1.29",
        kms_key_arn_for_secrets: Optional[str] = None,
        tags: Optional[dict] = None,
    ) -> None:
        super().__init__(scope, id)

        self.eks = TerraformModule(
            self,
            "eks",
            source="terraform-aws-modules/eks/aws",
            version="~> 20.0",
        )
        self.eks.add_override("cluster_name", cluster_name)
        self.eks.add_override("cluster_version", cluster_version)
        self.eks.add_override("vpc_id", vpc_id)
        self.eks.add_override("subnet_ids", private_subnet_ids)
        self.eks.add_override("enable_irsa", True)
        self.eks.add_override("cluster_endpoint_public_access", False)
        self.eks.add_override("cluster_endpoint_private_access", True)
        self.eks.add_override(
            "eks_managed_node_groups",
            {
                "default": {
                    "desired_size": 2,
                    "min_size": 2,
                    "max_size": 4,
                    "instance_types": ["t3.large"],
                    "capacity_type": "ON_DEMAND",
                    "labels": {"workload": "general"},
                    "tags": {
                        "k8s.io/cluster-autoscaler/enabled": "true",
                        f"k8s.io/cluster-autoscaler/{cluster_name}": "owned",
                    },
                }
            },
        )
        self.eks.add_override(
            "cluster_enabled_log_types",
            ["api", "audit", "authenticator", "controllerManager", "scheduler"],
        )
        if kms_key_arn_for_secrets:
            self.eks.add_override(
                "cluster_encryption_config",
                [{"resources": ["secrets"], "provider_key_arn": kms_key_arn_for_secrets}],
            )
        self.eks.add_override("tags", tags or {"Project": "supabase-on-eks", "ManagedBy": "cdktf"})

    @property
    def cluster_name(self) -> str:
        return self.eks.get_string("cluster_name")

    @property
    def oidc_provider_url(self) -> str:
        return self.eks.get_string("cluster_oidc_issuer_url")

    @property
    def oidc_provider_arn(self) -> str:
        return self.eks.get_string("oidc_provider_arn")

    @property
    def node_security_group_id(self) -> str:
        return self.eks.get_string("node_security_group_id")

    @property
    def kubeconfig_path(self) -> str:
        return f"./kubeconfig-{self.cluster_name}"
