import os
import sys
from os.path import dirname, join

if sys.version_info.minor == 7:
    import importlib_metadata as metadata
else:
    from importlib import metadata

__version__ = metadata.version(__name__)


# this line has to be executed before protobuf is imported
# https://github.com/protocolbuffers/protobuf/issues/3002#issuecomment-325459597
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

resource_dir = join(dirname(__file__), "resources")


__all__ = ["__version__", "resource_dir"]
