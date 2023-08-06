"""Legacy :mod:`builtins` module."""
from __future__ import absolute_import

# Add temporary imports.
import sys as __sys

# Import `builtins` members.
try:
    from builtins import *
    from builtins import __doc__
except ImportError:
    from __builtin__ import *
    from __builtin__ import __doc__
__all__ = sorted(__k for __k in globals().keys()
                 if not (__k.startswith("__") or __k.endswith("__")))

# Start with backports.
if __sys.version_info[:2] < (3, 2):

    # Backport info:
    # - Python 3.2: first appeareance.
    class ResourceWarning(Warning):
        """Base class for warnings about resource usage."""

    if "ResourceWarning" not in __all__:
        __all__.append("ResourceWarning")

if (3, 0) <= __sys.version_info[:2] < (3, 2):

    # Backport info:
    # - Python 3.0 and 3.1: removed from builtins.
    def callable(obj):
        """Return whether the object is callable (i.e., some kind of function).

        Note that classes are callable, as are instances of classes with a
        __call__() method."""

        return hasattr(obj, "__call__")

# Remove temporary imports.
del __sys
