from typing import Dict, List, Optional
from constructs import Construct
from cdktf_cdktf_provider_aws.eks_addon import EksAddon
from cdktf import TerraformResource


class EksAddons(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        cluster_name: str,
        addon_versions: Optional[Dict[str, Optional[str]]] = None,
        tags: Optional[dict] = None,
    ) -> None:
        super().__init__(scope, id)

        # Default addons; versions optional (pin in CI/CD when needed)
        addons = addon_versions or {
            "vpc-cni": None,
            "coredns": None,
            "kube-proxy": None,
            "aws-ebs-csi-driver": None,
        }
        for addon_name, version in addons.items():
            EksAddon(
                self,
                f"{addon_name.replace('-', '_')}",
                cluster_name=cluster_name,
                addon_name=addon_name,
                addon_version=version,
                tags=tags,
            )
