import pathlib

import pkg_resources

ROLE_PATH = pathlib.Path(
    pkg_resources.resource_filename("taktile_auth", "../assets/roles.yaml")
)
RESOURCE_PATH = pathlib.Path(
    pkg_resources.resource_filename("taktile_auth", "../assets/resources.yaml")
)
