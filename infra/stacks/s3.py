from constructs import Construct
from cdk_constructs.secure_bucket import SecureBucket
from typing import Optional


class StorageBucket(Construct):
    def __init__(self, scope: Construct, id: str, bucket_prefix: str = "supabase-storage-", use_kms: bool = False, kms_key_arn: Optional[str] = None, tags: Optional[dict] = None) -> None:
        super().__init__(scope, id)

        self.secure_bucket = SecureBucket(self, "secure_bucket", bucket_prefix=bucket_prefix, use_kms=use_kms, kms_key_arn=kms_key_arn, tags=tags)

    @property
    def bucket_name(self) -> str:
        return self.secure_bucket.name

    @property
    def bucket_arn(self) -> str:
        return self.secure_bucket.arn
