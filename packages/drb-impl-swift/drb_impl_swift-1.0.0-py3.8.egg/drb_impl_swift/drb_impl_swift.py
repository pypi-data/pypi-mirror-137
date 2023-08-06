import io
import os
from abc import ABC
from typing import Optional, Any, List, Dict, Tuple

from drb import AbstractNode, DrbNode
from drb.exceptions import DrbException
from drb.path import ParsedPath

from drb_impl_swift.swift_utils import Download, SwiftAuth, SwiftConnection


class SwiftNode(AbstractNode, ABC):
    """
    Common SwiftNode interface
    """

    def __init__(self, auth: SwiftAuth):
        super(SwiftNode, self).__init__()
        self._auth = auth
        self._swift = None

    def get_service_url(self) -> Optional[str]:
        """
        Returns URL of the swift auth service.

        :returns: string URL representation the swift auth service
        :rtype: str
        """
        return self._auth.authurl

    def get_storage(self) -> Optional[str]:
        """
        Returns URL of the swift storage.

        :returns: string URL representation the swift storage
        :rtype: str
        """
        return self._auth.preauthurl

    def get_auth(self) -> SwiftAuth:
        """
        Return the Auth object created to access the service.

        :returns: an Auth object.
        :rtype: SwiftAuth
        """
        return self._auth

    def close(self) -> None:
        """
        Close The swift connection
        """
        if self._swift is not None:
            self._swift.close()

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[Any]:
        return None

    def __eq__(self, other):
        return isinstance(other, SwiftNode) and \
               self._auth == other._auth

    def __hash__(self):
        return hash(self.auth)


class SwiftObject(SwiftNode):

    def __init__(self, path: str, obj: dict,
                 auth: SwiftAuth, parent: SwiftNode):
        super().__init__(auth)
        self._auth = self.get_auth()
        self._name = obj.get('name')
        self._path = os.path.join(path, self._name)
        self._attributes = obj
        self._children = None
        self._parent = parent

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return self._attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        if namespace_uri is None:
            try:
                return self._attributes[name]
            except KeyError:
                pass
        raise DrbException(f'No attribute found: ({name}, {namespace_uri})')

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> ParsedPath:
        return ParsedPath(self._path)

    @property
    def children(self) -> List[DrbNode]:
        return []

    def has_impl(self, impl: type) -> bool:
        return impl == io.BytesIO

    """
    These class allow the download of object in a container.

    Parameters:
        impl (type): The type supported by this implementation,
                     here only io.BytesIO is supported.
        chunk_size (int): The size of the chunk used during the download can
                          be set here (default: 12000).
    """
    def get_impl(self, impl: type, **kwargs) -> Any:
        self._swift = SwiftConnection(self._auth)

        if self.has_impl(impl):
            _, body = self._swift.get_object(container=self.parent.name,
                                             obj=self.name,
                                             resp_chunk_size=kwargs.get(
                                                 'chunk_size', 12000))
            return Download(body)
        raise DrbException(f'Not supported implementation: {impl}')

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        return False


class SwiftContainer(SwiftNode):

    def __init__(self, obj: dict, auth: SwiftAuth, parent: SwiftNode):
        super().__init__(auth)
        self._auth = auth
        self._name = obj.get('name')
        self._path = os.path.join(parent.name, self._name)
        self._attributes = obj
        self._children = None
        self._parent = parent

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return self._attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        if namespace_uri is None:
            try:
                return self._attributes[name]
            except KeyError:
                pass
        raise DrbException(f'No attribute found: ({name}, {namespace_uri})')

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> ParsedPath:
        return ParsedPath(self._path)

    @property
    def children(self) -> List[DrbNode]:
        self._swift = SwiftConnection(self._auth)
        if self._children is None:
            _, objects = self._swift.get_container(
                self._name, full_listing=True)
            self._children = [
                SwiftObject(self._path, obj, self._auth, self)
                for obj in objects]
        return self._children

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbException(
            f"SwiftService doesn't support {impl} implementation")

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if namespace is None:
            if name is not None:
                return name in [x.name for x in self.children]
            return len(self.children) > 0
        return False


class SwiftService(SwiftNode):

    def __init__(self, auth: SwiftAuth):
        super().__init__(auth)
        self._auth = auth
        self._attributes = {}
        self._children = None

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        self._swift = SwiftConnection(self._auth)
        self._attributes = self._swift.get_capabilities()
        return self._attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        if self._attributes is {}:
            self.attributes
        if namespace_uri is None:
            try:
                return self._attributes[name]
            except KeyError:
                pass
        raise DrbException(f'No attribute found: ({name}, {namespace_uri})')

    @property
    def parent(self) -> Optional[DrbNode]:
        return None

    @property
    def path(self) -> ParsedPath:
        return ParsedPath(os.path.sep)

    @property
    def children(self) -> List[DrbNode]:
        self._swift = SwiftConnection(self._auth)
        if self._children is None:
            _, containers = self._swift.get_account()
            self._children = [
                SwiftContainer(container, self._auth, self)
                for container in containers]
        return self._children

    @property
    def name(self) -> str:
        if self._auth.preauthurl:
            return self._auth.preauthurl
        return self._auth.authurl

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbException(
            f"SwiftService doesn't support {impl} implementation")

    def has_child(self, name: str = None, namespace: str = None) -> bool:
        if namespace is None:
            if name is not None:
                return name in [x.name for x in self.children]
            return len(self.children) > 0
        return False
