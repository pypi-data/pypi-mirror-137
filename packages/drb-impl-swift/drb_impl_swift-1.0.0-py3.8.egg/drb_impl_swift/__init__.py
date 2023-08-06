from . import _version

__version__ = _version.get_versions()['version']

from .drb_impl_swift import SwiftAuth, \
    SwiftObject, SwiftContainer, SwiftService

del _version

__all__ = [
    SwiftAuth,
    SwiftObject,
    SwiftContainer,
    SwiftService
]
