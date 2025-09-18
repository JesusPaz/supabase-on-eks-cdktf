from typing import Optional
from constructs import Construct
from cdktf_cdktf_provider_aws.s3_bucket import S3Bucket
from cdktf_cdktf_provider_aws.s3_bucket_public_access_block import S3BucketPublicAccessBlock
from cdktf_cdktf_provider_aws.s3_bucket_versioning import (
    S3BucketVersioningA,
    S3BucketVersioningVersioningConfiguration,
)
from cdktf_cdktf_provider_aws.s3_bucket_server_side_encryption_configuration import (
    S3BucketServerSideEncryptionConfigurationA,
    S3BucketServerSideEncryptionConfigurationRuleA,
    S3BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultA,
)
from cdktf_cdktf_provider_aws.s3_bucket_ownership_controls import (
    S3BucketOwnershipControls,
    S3BucketOwnershipControlsRule,
)
from cdktf_cdktf_provider_aws.s3_bucket_policy import S3BucketPolicy


class SecureBucket(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        bucket_prefix: Optional[str] = None,
        bucket_name: Optional[str] = None,
        use_kms: bool = False,
        kms_key_arn: Optional[str] = None,
        force_destroy: bool = False,
        tags: Optional[dict] = None,
    ) -> None:
        super().__init__(scope, id)

        self.bucket = S3Bucket(
            self,
            "bucket",
            bucket_prefix=bucket_prefix,
            bucket=bucket_name,
            force_destroy=force_destroy,
            tags=tags,
        )

        S3BucketPublicAccessBlock(
            self,
            "bpa",
            bucket=self.bucket.bucket,
            block_public_acls=True,
            block_public_policy=True,
            ignore_public_acls=True,
            restrict_public_buckets=True,
        )

        S3BucketVersioningA(
            self,
            "versioning",
            bucket=self.bucket.bucket,
            versioning_configuration=S3BucketVersioningVersioningConfiguration(status="Enabled"),
        )

        sse_default = (
            S3BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultA(
                sse_algorithm="aws:kms" if use_kms else "AES256",
                kms_master_key_id=kms_key_arn if use_kms else None,
            )
        )
        S3BucketServerSideEncryptionConfigurationA(
            self,
            "sse",
            bucket=self.bucket.bucket,
            rule=[
                S3BucketServerSideEncryptionConfigurationRuleA(
                    apply_server_side_encryption_by_default=sse_default,
                    bucket_key_enabled=True if use_kms else None,
                )
            ],
        )

        S3BucketOwnershipControls(
            self,
            "ownership",
            bucket=self.bucket.bucket,
            rule=S3BucketOwnershipControlsRule(object_ownership="BucketOwnerPreferred"),
        )

        S3BucketPolicy(
            self,
            "ssl_only_policy",
            bucket=self.bucket.bucket,
            policy='{'\
                   '  "Version": "2012-10-17",'\
                   '  "Statement": ['\
                   '    {'\
                   '      "Sid": "DenyInsecureTransport",'\
                   '      "Effect": "Deny",'\
                   '      "Principal": "*",'\
                   '      "Action": "s3:*",'\
                   '      "Resource": ['\
                   f'        "{self.bucket.arn}",'\
                   f'        "{self.bucket.arn}/*"'\
                   '      ],'\
                   '      "Condition": {'\
                   '        "Bool": {"aws:SecureTransport": "false"}'\
                   '      }'\
                   '    }'\
                   '  ]'\
                   '}'
        )

    @property
    def name(self) -> str:
        return self.bucket.bucket

    @property
    def arn(self) -> str:
        return self.bucket.arn
