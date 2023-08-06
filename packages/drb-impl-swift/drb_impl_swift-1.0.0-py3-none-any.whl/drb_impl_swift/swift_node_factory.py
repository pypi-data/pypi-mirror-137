from drb import DrbNode
from drb.factory.factory import DrbFactory

from drb_impl_swift import SwiftService


class SwiftNodeFactory(DrbFactory):

    @staticmethod
    def _create_from_uri_of_node(node: DrbNode):
        if isinstance(node, SwiftService):
            return node
        raise NotImplementedError("Call impl method")

    def _create(self, node: DrbNode) -> DrbNode:
        return self._create_from_uri_of_node(node)
