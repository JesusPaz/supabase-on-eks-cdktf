from constructs import Construct
from cdk_constructs.managed_secret import ManagedSecret
import json


class Secrets(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        db_endpoint: str = "",
        s3_bucket_name: str = "",
    ) -> None:
        super().__init__(scope, id)

        # JWT secrets (all in one secret as JSON)
        jwt_secrets = {
            "secret": "CHANGE_ME_SUPABASE_JWT_SECRET_32_CHARS_MIN",
            "anon_key": "CHANGE_ME_ANON_JWT_KEY",
            "service_role_key": "CHANGE_ME_SERVICE_ROLE_JWT_KEY"
        }
        ManagedSecret(
            self, 
            "jwt_secret", 
            name="supabase/jwt", 
            secret_string=json.dumps(jwt_secrets)
        )

        # Database secrets (all in one secret as JSON)
        # Extract hostname from RDS endpoint (remove port if present)
        db_host = db_endpoint.split(":")[0] if db_endpoint and ":" in db_endpoint else db_endpoint if db_endpoint else "CHANGE_ME_DB_HOST"
        
        db_secrets = {
            "username": "supabase",
            "password": "CHANGE_ME_DB_PASSWORD",
            "database": "supabase",
            "host": db_host
        }
        ManagedSecret(
            self, 
            "database_secret", 
            name="supabase/database", 
            secret_string=json.dumps(db_secrets)
        )

        # Analytics secrets
        analytics_secrets = {
            "logflare_api_key": "CHANGE_ME_LOGFLARE_API_KEY_32_CHARS_MIN"
        }
        ManagedSecret(
            self, 
            "analytics_secret", 
            name="supabase/analytics", 
            secret_string=json.dumps(analytics_secrets)
        )

        # Dashboard secrets
        dashboard_secrets = {
            "username": "supabase",
            "password": "CHANGE_ME_DASHBOARD_PASSWORD"
        }
        ManagedSecret(
            self, 
            "dashboard_secret", 
            name="supabase/dashboard", 
            secret_string=json.dumps(dashboard_secrets)
        )

        # S3 secrets (for chart compatibility, though IRSA is used)
        s3_secrets = {
            "bucket_name": s3_bucket_name or "CHANGE_ME_S3_BUCKET",
            "region": "us-east-1",
            "access_key_id": "NOT_USED_WITH_IRSA",
            "secret_access_key": "NOT_USED_WITH_IRSA"
        }
        ManagedSecret(
            self, 
            "s3_secret", 
            name="supabase/s3", 
            secret_string=json.dumps(s3_secrets)
        )
