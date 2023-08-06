# Copyright Exafunction, Inc.

_module_repository_clear_allowed = False
from exa.common_pb.common_pb2 import DataType
from exa.common_pb.common_pb2 import ModuleContextInfo
from exa.common_pb.common_pb2 import ModuleInfo
from exa.common_pb.common_pb2 import ValueMetadata
from exa.py_module_repository import *

# Enable partial distribution without actual client
try:
    from exa.py_client import *
    from exa.py_module import *
    from exa.py_value import *
except ImportError as e:
    import os

    if os.environ.get("EXA_DEBUG_IMPORT", False):
        print("Failed to import Exafunction modules")
        raise e

# Enable extra module distribution without dependencies
try:
    from exa.py_ffmpeg import *
except ImportError as e:
    import os

    if os.environ.get("EXA_DEBUG_IMPORT_EXTRAS", False):
        print("Failed to import Exafunction extras modules")
        raise e
