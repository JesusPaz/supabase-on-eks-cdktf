from typing import List
from constructs import Construct
from cdktf import TerraformModule
from cdktf_cdktf_provider_aws.security_group import SecurityGroup
from cdktf_cdktf_provider_aws.vpc_security_group_ingress_rule import VpcSecurityGroupIngressRule


class Rds(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        db_name: str,
        vpc_id: str,
        private_subnet_ids: List[str],
        eks_node_sg_id: str,
    ) -> None:
        super().__init__(scope, id)

        # Create security group for RDS
        self.rds_sg = SecurityGroup(
            self,
            "rds_security_group",
            name=f"{db_name}-rds-sg",
            description="Security group for RDS PostgreSQL database",
            vpc_id=vpc_id,
            tags={"Name": f"{db_name}-rds-sg", "Project": "supabase-on-eks"}
        )
        
        # Allow inbound PostgreSQL traffic from EKS nodes
        VpcSecurityGroupIngressRule(
            self,
            "rds_ingress_from_eks",
            security_group_id=self.rds_sg.id,
            from_port=5432,
            to_port=5432,
            ip_protocol="tcp",
            referenced_security_group_id=eks_node_sg_id,
            description="Allow PostgreSQL access from EKS nodes"
        )

        self.rds = TerraformModule(
            self,
            "rds",
            source="terraform-aws-modules/rds/aws",
        )
        self.rds.add_override("identifier", db_name)
        self.rds.add_override("engine", "postgres")
        self.rds.add_override("engine_version", "14")
        self.rds.add_override("family", "postgres14")
        self.rds.add_override("major_engine_version", "14")
        self.rds.add_override("instance_class", "db.t3.medium")
        self.rds.add_override("allocated_storage", 20)
        self.rds.add_override("max_allocated_storage", 100)
        self.rds.add_override("multi_az", True)
        self.rds.add_override("db_name", db_name)
        self.rds.add_override("username", "supabase")
        self.rds.add_override("manage_master_user_password", True)
        # Subnet configuration
        self.rds.add_override("subnet_ids", private_subnet_ids)
        self.rds.add_override("create_db_subnet_group", True)
        
        # Security group configuration
        self.rds.add_override("vpc_security_group_ids", [self.rds_sg.id])
        self.rds.add_override("deletion_protection", False)
        self.rds.add_override("skip_final_snapshot", True)
        self.rds.add_override("publicly_accessible", False)
        self.rds.add_override("backup_retention_period", 7)
        self.rds.add_override("backup_window", "03:00-06:00")
        self.rds.add_override("maintenance_window", "Sun:06:00-Sun:07:00")
        self.rds.add_override("storage_encrypted", True)
        self.rds.add_override("tags", {"Project": "supabase-on-eks", "ManagedBy": "cdktf"})

    @property
    def db_endpoint(self) -> str:
        return self.rds.get_string("db_instance_endpoint")

    @property
    def db_name(self) -> str:
        return self.rds.get_string("db_instance_name")

    @property
    def db_username(self) -> str:
        return self.rds.get_string("db_instance_username")

    @property
    def master_user_secret_arn(self) -> str:
        return self.rds.get_string("db_instance_master_user_secret_arn")
