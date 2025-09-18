from typing import List, Optional
from constructs import Construct
from cdktf import TerraformModule, IResolvable


class Network(Construct):
    def __init__(self, scope: Construct, id: str, vpc_name: str = "supabase-eks-vpc", tags: Optional[dict] = None) -> None:
        super().__init__(scope, id)

        self.vpc = TerraformModule(
            self,
            "vpc",
            source="terraform-aws-modules/vpc/aws",
            version="~> 5.0",
        )
        self.vpc.add_override("name", vpc_name)
        self.vpc.add_override("cidr", "10.0.0.0/16")
        self.vpc.add_override("azs", ["us-east-1a", "us-east-1b", "us-east-1c"])
        self.vpc.add_override("private_subnets", ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"])
        self.vpc.add_override("public_subnets", ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"])
        self.vpc.add_override("enable_nat_gateway", True)
        self.vpc.add_override("single_nat_gateway", True)
        self.vpc.add_override("enable_dns_hostnames", True)
        self.vpc.add_override("enable_dns_support", True)
        self.vpc.add_override("create_igw", True)
        self.vpc.add_override("enable_dhcp_options", True)
        self.vpc.add_override("tags", tags or {"Project": "supabase-on-eks", "ManagedBy": "cdktf"})

    @property
    def vpc_id(self) -> str:
        return self.vpc.get_string("vpc_id")

    @property
    def private_subnet_ids(self) -> IResolvable:
        return self.vpc.interpolation_for_output("private_subnets")

    @property
    def public_subnet_ids(self) -> IResolvable:
        return self.vpc.interpolation_for_output("public_subnets")

    @property
    def private_route_table_ids(self) -> IResolvable:
        return self.vpc.interpolation_for_output("private_route_table_ids")
