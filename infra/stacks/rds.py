from typing import List
from constructs import Construct
from cdktf import TerraformModule


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
        self.rds.add_override("create_random_password", False)
        self.rds.add_override("subnet_ids", private_subnet_ids)
        self.rds.add_override("create_db_subnet_group", True)
        self.rds.add_override(
            "security_group_rules",
            {
                "from_nodes": {
                    "type": "ingress",
                    "from_port": 5432,
                    "to_port": 5432,
                    "protocol": "tcp",
                    "source_security_group_id": eks_node_sg_id,
                    "description": "Allow Postgres from EKS nodes",
                }
            },
        )
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
        return self.rds.get_string("db_name")

    @property
    def db_username(self) -> str:
        return self.rds.get_string("db_instance_username")

    @property
    def master_user_secret_arn(self) -> str:
        return self.rds.get_string("db_instance_master_user_secret_arn")
