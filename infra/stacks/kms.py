from typing import Optional
from constructs import Construct
from cdk_constructs.kms_key import KmsKeyConstruct


class KmsStack(Construct):
    def __init__(self, scope: Construct, id: str, project: str, environment: str, tags: Optional[dict] = None) -> None:
        super().__init__(scope, id)
        self.s3 = KmsKeyConstruct(
            self,
            "s3",
            description=f"KMS key for S3 encryption ({project}-{environment})",
            alias=f"{project}-{environment}-s3",
            tags=tags,
        )
        self.eks = KmsKeyConstruct(
            self,
            "eks",
            description=f"KMS key for EKS secrets encryption ({project}-{environment})",
            alias=f"{project}-{environment}-eks",
            tags=tags,
        )

    @property
    def s3_key_arn(self) -> str:
        return self.s3.arn

    @property
    def eks_key_arn(self) -> str:
        return self.eks.arn
