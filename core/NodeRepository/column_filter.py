import pandas as pd


def column_filter(settings, input_ports):
    input_1 = input_ports["port_1"]
    columns = settings["columns"]

    output_1 = pd.DataFrame(input_1)
    output_1 = output_1.filter(columns)

    output_1 = output_1.to_dict(orient='records')

    return {
        "port_1": output_1
    }
