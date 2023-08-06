from taktile_auth.entities import Permission
from taktile_auth.parser import RESOURCES
from taktile_auth.parser.utils import parse_permission


def build_query(query: str) -> Permission:

    parsed_query = parse_permission(query)
    fields = list(RESOURCES[parsed_query["resource_name"]].args.keys())
    resource_vals = {
        fields[x]: parsed_query["resource_args"][x] for x in range(len(fields))
    }
    return Permission(
        actions=set(parsed_query["actions"]),
        resource=RESOURCES[parsed_query["resource_name"]].get_resource()(
            **resource_vals
        ),
    )
