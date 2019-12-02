import sys
from os import walk

import pandas as pd

from Node import Node
import NodeRepository


class UnitTest:
    # Give node names to test as command line arguments
    # If you don't test will apply for all nodes
    def __init__(self, command_line_arguments):
        self.command_line_arguments = command_line_arguments

    def run_test(self):
        command_line_arguments = self.command_line_arguments
        if len(command_line_arguments) == 0:
            f = []
            for (dirpath, dirnames, filenames) in walk("NodeRepository"):
                f.extend(filenames)
                break
            for filename in f:
                if filename[:5] == "test_":
                    command_line_arguments.append(filename[5:-3])

        for node_name in command_line_arguments:
            file_name = "test_" + node_name
            output_ports = getattr(NodeRepository, file_name)(
                Node
            )

            for port in output_ports.keys():
                output_table = output_ports[port]
                output_table = pd.DataFrame(output_table)
                output_table = output_table.head()
                if type(output_table) == pd.core.frame.DataFrame:
                    print(node_name + " --> " + port + ": ok")
                else:
                    print(node_name + " --> " + port + ": not ok")


if __name__ == '__main__':

    command_line_arguments = sys.argv[1:]

    UT = UnitTest(command_line_arguments)
    output_ports = UT.run_test()
