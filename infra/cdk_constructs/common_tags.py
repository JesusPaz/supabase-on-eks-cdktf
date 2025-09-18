from typing import Dict, Optional
from constructs import Construct


class CommonTags(Construct):
    def __init__(self, scope: Construct, id: str, project: str, environment: str, owner: Optional[str] = None, cost_center: Optional[str] = None) -> None:
        super().__init__(scope, id)
        self._tags: Dict[str, str] = {
            "Project": project,
            "Environment": environment,
            "ManagedBy": "cdktf",
        }
        if owner:
            self._tags["Owner"] = owner
        if cost_center:
            self._tags["CostCenter"] = cost_center

    @property
    def tags(self) -> Dict[str, str]:
        return dict(self._tags)
