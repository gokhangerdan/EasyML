import pandas as pd


def test_column_filter(Node):
    request_body = {
        "function": "column_filter",
        "settings": {
            "columns": ["Name"]
        },
        "input_ports": {
            "port_1": pd.read_csv("sample_datasets/titanic.csv").to_dict(
                orient='records'
            )
        }
    }

    node = Node(
        function=request_body["function"],
        settings=request_body["settings"],
        input_ports=request_body["input_ports"]
    )

    return node.output_ports
