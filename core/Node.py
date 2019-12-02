import sys

import NodeRepository

sys.path.append("core")


class Node:
    def __init__(self, function, settings, input_ports=None):
        function = getattr(NodeRepository, function)
        self.output_ports = function(settings, input_ports)
