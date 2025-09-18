from typing import List, Optional, Union
from constructs import Construct
from cdktf_cdktf_provider_aws.vpc_endpoint import VpcEndpoint


class VpcEndpoints(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        vpc_id: str,
        private_subnet_ids: Union[List[str], object],
        private_route_table_ids: Optional[Union[List[str], object]],
        region: str = "us-east-1",
        security_group_ids: Optional[List[str]] = None,
        tags: Optional[dict] = None,
    ) -> None:
        super().__init__(scope, id)

        # Gateway endpoint for S3 only if we have concrete route table ids
        if isinstance(private_route_table_ids, list):
            VpcEndpoint(
                self,
                "s3_gateway",
                vpc_id=vpc_id,
                service_name=f"com.amazonaws.{region}.s3",
                vpc_endpoint_type="Gateway",
                route_table_ids=private_route_table_ids,
                tags=tags,
            )

        # Interface endpoints - only create if we have concrete subnet IDs
        if isinstance(private_subnet_ids, list):
            services = [
                "secretsmanager",
                "ecr.api",
                "ecr.dkr",
                "sts",
                "logs",
                "ec2",
            ]
            for svc in services:
                VpcEndpoint(
                    self,
                    f"iface_{svc.replace('.', '_')}",
                    vpc_id=vpc_id,
                    service_name=f"com.amazonaws.{region}.{svc}",
                    vpc_endpoint_type="Interface",
                    private_dns_enabled=True,
                    subnet_ids=private_subnet_ids,
                    security_group_ids=security_group_ids,
                    tags=tags,
                )
