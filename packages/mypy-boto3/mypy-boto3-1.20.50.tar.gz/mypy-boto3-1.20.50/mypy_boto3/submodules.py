import importlib
import importlib.util
from typing import List


class Submodule:
    def __init__(
        self,
        module_name: str,
        import_name: str,
        boto3_name: str,
        class_name: str,
        pypi_name: str,
        has_resource: bool,
        has_waiter: bool,
        has_paginator: bool,
    ):
        self.module_name = module_name
        self.import_name = import_name
        self.boto3_name = boto3_name
        self.class_name = class_name
        self.pypi_name = pypi_name
        self.has_resource = has_resource
        self.has_waiter = has_waiter
        self.has_paginator = has_paginator
        self.is_installed = importlib.util.find_spec(module_name) is not None
        self.is_active = self.is_installed

    def get_all_names(self) -> List[str]:
        service_module = importlib.import_module(self.module_name)
        return getattr(service_module, "__all__", [])


SUBMODULES: List[Submodule] = [
    Submodule(
        module_name="mypy_boto3_auditmanager",
        import_name="auditmanager",
        boto3_name="auditmanager",
        class_name="AuditManager",
        pypi_name="mypy-boto3-auditmanager",
        has_resource=False,
        has_waiter=False,
        has_paginator=False,
    ),
    Submodule(
        module_name="mypy_boto3_synthetics",
        import_name="synthetics",
        boto3_name="synthetics",
        class_name="Synthetics",
        pypi_name="mypy-boto3-synthetics",
        has_resource=False,
        has_waiter=False,
        has_paginator=False,
    ),
    Submodule(
        module_name="mypy_boto3_ssm_incidents",
        import_name="ssm_incidents",
        boto3_name="ssm-incidents",
        class_name="SSMIncidents",
        pypi_name="mypy-boto3-ssm-incidents",
        has_resource=False,
        has_waiter=True,
        has_paginator=True,
    ),
    Submodule(
        module_name="mypy_boto3_events",
        import_name="events",
        boto3_name="events",
        class_name="EventBridge",
        pypi_name="mypy-boto3-events",
        has_resource=False,
        has_waiter=False,
        has_paginator=True,
    ),
]
