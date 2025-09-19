from constructs import Construct
from cdktf import TerraformAsset, AssetType, TerraformOutput, Token
from cdktf_cdktf_provider_aws.lambda_function import LambdaFunction
from cdktf_cdktf_provider_aws.lambda_permission import LambdaPermission
from cdktf_cdktf_provider_aws.iam_role import IamRole
from cdktf_cdktf_provider_aws.iam_role_policy_attachment import IamRolePolicyAttachment
from cdktf_cdktf_provider_aws.iam_policy import IamPolicy
from cdktf_cdktf_provider_aws.cloudformation_stack import CloudformationStack
from cdktf_cdktf_provider_aws.security_group import SecurityGroup
from cdktf_cdktf_provider_aws.security_group_rule import SecurityGroupRule
from cdktf_cdktf_provider_aws.secretsmanager_secret import SecretsmanagerSecret
from cdktf_cdktf_provider_aws.secretsmanager_secret_version import SecretsmanagerSecretVersion
import json
import os


class DatabaseMigrations(Construct):
    """
    Database Migration Lambda Functions for Supabase
    Based on the original CDK solution but adapted for CDKTF
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc_id: str,
        private_subnet_ids: list,
        db_secret_arn: str,
        db_endpoint: str,
        db_port: int = 5432,
        tags: dict = None,
    ):
        super().__init__(scope, construct_id)

        self.vpc_id = vpc_id
        self.private_subnet_ids = private_subnet_ids
        self.db_secret_arn = db_secret_arn
        self.db_endpoint = db_endpoint
        self.db_port = db_port
        self.tags = tags or {}

        # Create security group for Lambda functions
        self._create_lambda_security_group()
        
        # Update RDS security group to allow Lambda access
        self._update_rds_security_group()
        
        # Create IAM roles and policies
        self._create_iam_roles()
        
        # Create Lambda functions
        self._create_migration_lambda()
        self._create_user_password_lambda()
        
        # Create custom resource for database migration
        self._create_migration_custom_resource()

    def _create_lambda_security_group(self):
        """Create security group for Lambda functions"""
        self.lambda_sg = SecurityGroup(
            self,
            "lambda_sg",
            name_prefix="supabase-db-lambda-",
            description="Security group for Supabase database Lambda functions",
            vpc_id=self.vpc_id,
            tags={**self.tags, "Name": "supabase-db-lambda-sg"}
        )

        # Allow outbound HTTPS for AWS APIs
        SecurityGroupRule(
            self,
            "lambda_sg_egress_https",
            type="egress",
            from_port=443,
            to_port=443,
            protocol="tcp",
            cidr_blocks=["0.0.0.0/0"],
            security_group_id=self.lambda_sg.id
        )

        # Allow outbound to PostgreSQL
        SecurityGroupRule(
            self,
            "lambda_sg_egress_postgres",
            type="egress",
            from_port=self.db_port,
            to_port=self.db_port,
            protocol="tcp",
            cidr_blocks=["10.0.0.0/8"],  # VPC CIDR range
            security_group_id=self.lambda_sg.id
        )

    def _update_rds_security_group(self):
        """Update RDS security group to allow Lambda access"""
        # Note: We'll need to get the RDS security group ID from the RDS stack
        # For now, we'll create a rule that allows access from our Lambda SG
        # This will need to be coordinated with the RDS stack
        pass

    def _create_iam_roles(self):
        """Create IAM roles and policies for Lambda functions"""
        
        # Migration Lambda Role
        self.migration_role = IamRole(
            self,
            "migration_role",
            name="supabase-db-migration-lambda-role",
            assume_role_policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "sts:AssumeRole",
                        "Effect": "Allow",
                        "Principal": {"Service": "lambda.amazonaws.com"}
                    }
                ]
            }),
            tags=self.tags
        )

        # User Password Lambda Role
        self.user_password_role = IamRole(
            self,
            "user_password_role",
            name="supabase-db-user-password-lambda-role",
            assume_role_policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "sts:AssumeRole",
                        "Effect": "Allow",
                        "Principal": {"Service": "lambda.amazonaws.com"}
                    }
                ]
            }),
            tags=self.tags
        )

        # Basic Lambda execution policy
        IamRolePolicyAttachment(
            self,
            "migration_basic_policy",
            role=self.migration_role.name,
            policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
        )

        IamRolePolicyAttachment(
            self,
            "user_password_basic_policy",
            role=self.user_password_role.name,
            policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
        )

        # Custom policy for Secrets Manager access
        secrets_policy = IamPolicy(
            self,
            "secrets_policy",
            name="supabase-db-secrets-policy",
            description="Policy for Supabase database Lambda functions to access secrets",
            policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": [
                            "secretsmanager:GetSecretValue"
                        ],
                        "Resource": self.db_secret_arn
                    }
                ]
            }),
            tags=self.tags
        )

        # User password specific policy
        user_password_policy = IamPolicy(
            self,
            "user_password_policy",
            name="supabase-db-user-password-policy",
            description="Policy for user password Lambda to manage user secrets",
            policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": [
                            "secretsmanager:GetSecretValue",
                            "secretsmanager:PutSecretValue",
                            "secretsmanager:CreateSecret",
                            "secretsmanager:UpdateSecret"
                        ],
                        "Resource": "arn:aws:secretsmanager:*:*:secret:supabase-*"
                    }
                ]
            }),
            tags=self.tags
        )

        # Attach policies
        IamRolePolicyAttachment(
            self,
            "migration_secrets_policy",
            role=self.migration_role.name,
            policy_arn=secrets_policy.arn
        )

        IamRolePolicyAttachment(
            self,
            "user_password_secrets_policy",
            role=self.user_password_role.name,
            policy_arn=secrets_policy.arn
        )

        IamRolePolicyAttachment(
            self,
            "user_password_manage_policy",
            role=self.user_password_role.name,
            policy_arn=user_password_policy.arn
        )

    def _create_migration_lambda(self):
        """Create the database migration Lambda function"""
        
        # Create asset for Lambda code
        migration_asset = TerraformAsset(
            self,
            "migration_asset",
            path=os.path.join(os.path.dirname(__file__), "..", "lambda", "db-migrations"),
            type=AssetType.ARCHIVE
        )

        self.migration_lambda = LambdaFunction(
            self,
            "migration_lambda",
            function_name="supabase-db-migrations",
            description="Supabase - Database migration function",
            filename=migration_asset.path,
            handler="index.handler",
            runtime="nodejs20.x",
            timeout=300,  # 5 minutes
            memory_size=512,
            role=self.migration_role.arn,
            environment={
                "variables": {
                    "DB_SECRET_ARN": self.db_secret_arn,
                    "DB_HOST": self.db_endpoint  # RDS address without port
                }
            },
            # VPC Configuration to access RDS
            vpc_config={
                "subnet_ids": Token.as_list(self.private_subnet_ids),
                "security_group_ids": [self.lambda_sg.id]
            },
            tags=self.tags
        )

    def _create_user_password_lambda(self):
        """Create the user password management Lambda function"""
        
        # Create asset for Lambda code  
        user_password_asset = TerraformAsset(
            self,
            "user_password_asset", 
            path=os.path.join(os.path.dirname(__file__), "..", "lambda", "user-password"),
            type=AssetType.ARCHIVE
        )

        self.user_password_lambda = LambdaFunction(
            self,
            "user_password_lambda",
            function_name="supabase-db-user-password",
            description="Supabase - DB user password function",
            filename=user_password_asset.path,
            handler="index.handler",
            runtime="nodejs20.x",
            timeout=60,
            memory_size=256,
            role=self.user_password_role.arn,
            environment={
                "variables": {
                    "DB_SECRET_ARN": self.db_secret_arn,
                    "DB_HOST": self.db_endpoint  # RDS address without port
                }
            },
            # VPC Configuration to access RDS
            vpc_config={
                "subnet_ids": Token.as_list(self.private_subnet_ids),
                "security_group_ids": [self.lambda_sg.id]
            },
            tags=self.tags
        )

    def _create_migration_custom_resource(self):
        """Create CloudFormation custom resource to trigger migrations"""
        
        # Calculate fingerprint of SQL files for change detection
        sql_dir = os.path.join(os.path.dirname(__file__), "..", "lambda", "db-migrations", "sql")
        fingerprint = self._calculate_sql_fingerprint(sql_dir)
        
        # CloudFormation template for custom resource
        cf_template = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Resources": {
                "DatabaseMigration": {
                    "Type": "AWS::CloudFormation::CustomResource",
                    "Properties": {
                        "ServiceToken": self.migration_lambda.arn,
                        "Fingerprint": fingerprint
                    }
                }
            },
            "Outputs": {
                "MigrationStatus": {
                    "Value": {"Ref": "DatabaseMigration"},
                    "Description": "Database migration status"
                }
            }
        }

        self.migration_stack = CloudformationStack(
            self,
            "migration_stack",
            name="supabase-db-migrations-v4",
            template_body=json.dumps(cf_template),
            capabilities=["CAPABILITY_IAM"],
            tags=self.tags
        )

        # Allow CloudFormation to invoke the Lambda
        LambdaPermission(
            self,
            "migration_lambda_permission",
            statement_id="AllowCloudFormationInvoke",
            action="lambda:InvokeFunction",
            function_name=self.migration_lambda.function_name,
            principal="cloudformation.amazonaws.com"
        )

    def _calculate_sql_fingerprint(self, sql_dir: str) -> str:
        """Calculate a fingerprint of SQL files for change detection"""
        import hashlib
        
        if not os.path.exists(sql_dir):
            return "no-sql-files"
        
        file_hashes = []
        for root, dirs, files in os.walk(sql_dir):
            for file in sorted(files):
                if file.endswith('.sql'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                        file_hashes.append(f"{file}:{file_hash}")
        
        combined = "|".join(file_hashes)
        return hashlib.md5(combined.encode()).hexdigest()

    @property
    def migration_lambda_arn(self) -> str:
        return self.migration_lambda.arn

    @property
    def user_password_lambda_arn(self) -> str:
        return self.user_password_lambda.arn

    @property
    def lambda_security_group_id(self) -> str:
        return self.lambda_sg.id

    def gen_user_password(self, username: str) -> SecretsmanagerSecret:
        """
        Generate and set password to database user
        Similar to the original CDK implementation
        """
        # Create a construct scope for the user
        user_construct = Construct(self, f"user_{username}")
        
        # Create user secret with auto-generated password
        user_secret = SecretsmanagerSecret(
            user_construct,
            "secret",
            name=f"supabase-db-{username}",
            description=f"Supabase - Database User {username}",
            generate_secret_string={
                "exclude_punctuation": True,
                "secret_string_template": json.dumps({"username": username}),
                "generate_string_key": "password"
            },
            tags={**self.tags, "Username": username}
        )
        
        # Create CloudFormation custom resource to set user password
        user_password_resource = CloudformationStack(
            user_construct,
            "password_resource",
            name=f"supabase-user-password-{username}",
            template_body=json.dumps({
                "AWSTemplateFormatVersion": "2010-09-09",
                "Resources": {
                    "UserPasswordResource": {
                        "Type": "Custom::DatabaseUserPassword",
                        "Properties": {
                            "ServiceToken": self.user_password_lambda.arn,
                            "Username": username,
                            "SecretId": user_secret.arn
                        }
                    }
                },
                "Outputs": {
                    "PhysicalResourceId": {
                        "Value": {"Ref": "UserPasswordResource"}
                    }
                }
            }),
            tags={**self.tags, "Username": username}
        )
        
        # Ensure user password resource depends on migration completion
        user_password_resource.add_override("depends_on", [self.migration_stack.name])
        
        return user_secret
