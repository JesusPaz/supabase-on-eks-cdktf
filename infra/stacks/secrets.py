from constructs import Construct
from cdk_constructs.managed_secret import ManagedSecret


class Secrets(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
    ) -> None:
        super().__init__(scope, id)

        ManagedSecret(self, "jwt_secret", name="supabase/jwt", secret_string="CHANGE_ME_SUPABASE_JWT_SECRET")
        ManagedSecret(self, "anon_key", name="supabase/anon_key", secret_string="CHANGE_ME_ANON_KEY")
        ManagedSecret(self, "service_key", name="supabase/service_key", secret_string="CHANGE_ME_SERVICE_ROLE_KEY")
