
import importlib.metadata
import pathlib

package = pathlib.Path(__file__).parent.name

try:
    __version__ = importlib.metadata.version(package)
except importlib.metadata.PackageNotFoundError:
    __version__ = None


