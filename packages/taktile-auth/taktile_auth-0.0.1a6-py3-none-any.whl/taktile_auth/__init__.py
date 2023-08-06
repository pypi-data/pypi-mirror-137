"""
Taktile Auth
"""
import pkg_resources

__version__ = pkg_resources.get_distribution(
    __name__.split(".", maxsplit=1)[0]
).version

from taktile_auth.entities import Permission, Role  # noqa: 401
from taktile_auth.parser import RESOURCES, ROLES  # noqa: 401
from taktile_auth.utils import build_query, parse_role  # noqa: 401
