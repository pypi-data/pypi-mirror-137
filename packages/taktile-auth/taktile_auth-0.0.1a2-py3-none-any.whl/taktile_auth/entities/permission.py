import re
import typing as t

import pydantic

from taktile_auth.entities.resource import Resource, ResourceDefinition
from taktile_auth.enums import Action


class Permission(pydantic.BaseModel):
    actions: t.Set[Action]
    resource: Resource

    def __contains__(self, query: "Permission") -> bool:
        action_match = query.actions.difference(self.actions) == set()
        resource_match = True
        for field in self.resource.dict().keys():
            allowed = getattr(self.resource, field)
            queried = getattr(query.resource, field)
            if not re.fullmatch(
                allowed.replace("*", ".*"), queried
            ):  # TODO - Beware of regex fails
                resource_match = False
                break
        return action_match and resource_match

    def __repr__(self) -> str:
        actions = "+".join(sorted(self.actions))
        resource_name = type(self.resource).__name__
        vals = ",".join(self.resource.dict().values())
        return f"{actions}:{resource_name}/{vals}"


Permission.update_forward_refs()


class PermissionDefinition(pydantic.BaseModel):
    actions: t.Set[Action]
    resource_definition: ResourceDefinition

    def build(self, **kwargs) -> Permission:
        extra_args = {
            arg: "*"
            for arg in set(self.resource_definition.args.keys()).difference(
                kwargs
            )
        }
        return Permission(
            actions=self.actions,
            resource=self.resource_definition.get_resource()(
                **kwargs, **extra_args
            ),
        )
