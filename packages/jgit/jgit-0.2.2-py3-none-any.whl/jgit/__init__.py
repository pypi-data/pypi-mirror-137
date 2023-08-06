
__all__ = (
)
import importlib.metadata

try:
    __version__ = importlib.metadata.version("package-name")
except importlib.metadata.PackageNotFoundError:
    __version__ = None

def app():
    print(__version__)

