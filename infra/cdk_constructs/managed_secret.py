from constructs import Construct
from cdktf_cdktf_provider_aws.secretsmanager_secret import SecretsmanagerSecret
from cdktf_cdktf_provider_aws.secretsmanager_secret_version import SecretsmanagerSecretVersion


class ManagedSecret(Construct):
    def __init__(self, scope: Construct, id: str, name: str, secret_string: str) -> None:
        super().__init__(scope, id)
        self.secret = SecretsmanagerSecret(self, "secret", name=name)
        self.version = SecretsmanagerSecretVersion(
            self,
            "version",
            secret_id=self.secret.id,
            secret_string=secret_string,
        )

    @property
    def arn(self) -> str:
        return self.secret.arn

    @property
    def name(self) -> str:
        return self.secret.name
