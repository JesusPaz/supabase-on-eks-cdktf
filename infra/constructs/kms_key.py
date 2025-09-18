from typing import Optional
from constructs import Construct
from cdktf_cdktf_provider_aws.kms_key import KmsKey
from cdktf_cdktf_provider_aws.kms_alias import KmsAlias


class KmsKeyConstruct(Construct):
    def __init__(self, scope: Construct, id: str, description: str, alias: Optional[str] = None, tags: Optional[dict] = None) -> None:
        super().__init__(scope, id)
        self.key = KmsKey(
            self,
            "key",
            description=description,
            enable_key_rotation=True,
            deletion_window_in_days=30,
            is_enabled=True,
            tags=tags,
        )
        if alias:
            KmsAlias(self, "alias", name=f"alias/{alias}", target_key_id=self.key.key_id)

    @property
    def arn(self) -> str:
        return self.key.arn
