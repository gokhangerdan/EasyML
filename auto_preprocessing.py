import pandas as pd
import numpy as np


class EnvironmentVariables:
    sample_datasets_path = "core/sample_datasets/"
    unique_identifier_treshold = 0.7
    max_correlation_treshold = 0.95
    unique_observations_treshold = 10


# Target must be categoric variable
class PreProcessingEngine:
    def __init__(self, dataframe, target_column=False):
        if target_column:
            self.dataframe = dataframe.drop(columns=[target_column])
            self.target_column = dataframe.filter([target_column])
        else:
            self.dataframe = dataframe

    def missing_value_handling(self):
        dataframe = self.dataframe
        dataframe = dataframe.interpolate()
        contains_null = dataframe.columns[dataframe.isnull().any()]
        categoric_missing_variables = dataframe.select_dtypes(
            include=[np.object]
        ).columns.tolist()
        categoric_missing_variables = [
            variable for variable in categoric_missing_variables if (
                variable in contains_null
            )
        ]
        for variable in categoric_missing_variables:
            data = dataframe[variable].tolist()
            unique_observations = list(set(data))
            counts = []
            for observation in unique_observations:
                counts.append(data.count(observation))
            most_frequent = unique_observations[counts.index(max(counts))]
            dataframe[variable] = dataframe[variable].fillna(most_frequent)
        self.dataframe = dataframe

    def check_unique_identifiers(self):
        dataframe = self.dataframe
        filter_container = []
        for column in dataframe.columns:
            observation_count = len(dataframe[column].tolist())
            unique_observation_count = len(set(dataframe[column].tolist()))
            if (
                unique_observation_count / observation_count
            ) >= EnvironmentVariables.unique_identifier_treshold:
                filter_container.append(column)
        dataframe = dataframe.drop(columns=filter_container)
        self.dataframe = dataframe

    def drop_datetime_variables(self):
        dataframe = self.dataframe
        datetime_variables = dataframe.select_dtypes(
            include=[np.datetime64]
        ).columns.tolist()
        dataframe = dataframe.drop(columns=datetime_variables)
        self.dataframe = dataframe

    def correlation_filter(self):
        dataframe = self.dataframe
        correlation_matrix = dataframe.corr().abs()
        upper_triangle = correlation_matrix.where(
            np.triu(np.ones(correlation_matrix.shape), k=1).astype(np.bool)
        )
        over_correlation = []
        for column in upper_triangle.columns:
            if any(
                upper_triangle[column] >
                EnvironmentVariables.max_correlation_treshold
            ):
                over_correlation.append(column)
        dataframe = dataframe.drop(columns=over_correlation)
        self.dataframe = dataframe

    def convert_data_types(self):
        dataframe = self.dataframe
        numeric_variables = dataframe.select_dtypes(
            exclude=[np.object]
        ).columns.tolist()
        for variable in numeric_variables:
            unique_observations = dataframe[variable].tolist()
            unique_observations = list(set(unique_observations))
            unique_observations = len(unique_observations)
            if (
                unique_observations <=
                EnvironmentVariables.unique_observations_treshold
            ):
                dataframe[variable] = dataframe[variable].apply(
                    lambda x: "variable_" + str(x)
                )
        categoric_variables = dataframe.select_dtypes(
            include=[np.object]
        ).columns.tolist()
        save_memory = []
        for variable in categoric_variables:
            unique_observations = dataframe[variable].tolist()
            unique_observations = list(set(unique_observations))
            unique_observations = len(unique_observations)
            if (
                unique_observations >
                EnvironmentVariables.unique_observations_treshold
            ):
                save_memory.append(variable)
        dataframe = dataframe.drop(columns=save_memory)
        categoric_variables = dataframe.select_dtypes(
            include=[np.object]
        ).columns.tolist()
        dataframe = pd.get_dummies(dataframe, prefix=categoric_variables)
        self.dataframe = dataframe

    def normalizer(self):
        dataframe = self.dataframe
        numeric_variables = dataframe.select_dtypes(
            exclude=[np.object]
        ).columns.tolist()
        for variable in numeric_variables:
            data = list(set(dataframe[variable].tolist()))
            min_value = min(data)
            max_value = max(data)
            dataframe[variable] = dataframe[variable].apply(
                lambda x: (x-min_value)/(max_value-min_value)
            )
        self.dataframe = dataframe


if __name__ == '__main__':
    import time

    t = time.time()

    file_names = [
        "bigquery-geotab-intersection-congestion.csv",
        "house-prices-advanced-regression-techniques.csv",
        "pubg-finish-placement-prediction.csv",
        "santander-customer-transaction-prediction.csv",
        "titanic.csv"
    ]

    for file_name in file_names:

        dataframe = pd.read_csv(
            EnvironmentVariables.sample_datasets_path +
            file_name
        )

        print("\nGet Data")
        amle = PreProcessingEngine(dataframe)
        print(amle.dataframe)
        print(amle.dataframe.columns)
        print(amle.dataframe.dtypes)
        print(amle.dataframe.describe())

        print("\nRemove Observations Which Contained Any Missing Value")
        amle.missing_value_handling()
        print(amle.dataframe)
        print(amle.dataframe.columns)
        print(amle.dataframe.dtypes)
        print(amle.dataframe.describe())

        print("\nDrop Id Variables")
        amle.check_unique_identifiers()
        print(amle.dataframe)
        print(amle.dataframe.columns)
        print(amle.dataframe.dtypes)
        print(amle.dataframe.describe())

        print("\nDrop DateTime Variables")
        amle.drop_datetime_variables()
        print(amle.dataframe)
        print(amle.dataframe.columns)
        print(amle.dataframe.dtypes)
        print(amle.dataframe.describe())

        print("\nDrop High Correlated Variables")
        amle.correlation_filter()
        print(amle.dataframe)
        print(amle.dataframe.columns)
        print(amle.dataframe.dtypes)
        print(amle.dataframe.describe())

        print("\nConvert Data Types")
        amle.convert_data_types()
        print(amle.dataframe)
        print(amle.dataframe.columns)
        print(amle.dataframe.dtypes)
        print(amle.dataframe.describe())

        print("\nNormalize Variables Between 0 - 1")
        amle.normalizer()
        print(amle.dataframe)
        print(amle.dataframe.columns)
        print(amle.dataframe.dtypes)
        print(amle.dataframe.describe())

    print("\n")
    print(time.time()-t)
