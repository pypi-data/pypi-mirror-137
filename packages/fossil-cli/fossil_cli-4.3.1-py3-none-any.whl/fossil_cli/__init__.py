import pkg_resources
from click import group, version_option

from .Branch import branch
from .Commit import commit
from .Info import info
from .New import new
from .Version import version

try:
    __version__ = pkg_resources.get_distribution("fossil-cli").version
except pkg_resources.DistributionNotFound:  # pragma: no cover
    __version__ = "unknown"


@group()
@version_option(version=__version__)
def cli():
    """Script para manejar un repositorio fossil de forma inteligente"""


cli.add_command(new)
cli.add_command(new, "init")

cli.add_command(version)
cli.add_command(version, "v")

cli.add_command(info)

cli.add_command(commit)
cli.add_command(commit, "c")

cli.add_command(branch)
cli.add_command(branch, "br")
