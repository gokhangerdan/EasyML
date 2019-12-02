import pandas as pd


def column_rename(settings, input_ports):
    input_1 = input_ports["port_1"]
    columns = settings["columns"]

    output_1 = pd.DataFrame(input_1)
    output_1 = output_1.rename(columns=columns)

    output_1 = output_1.to_dict(orient='records')

    return {
        "port_1": output_1
    }
