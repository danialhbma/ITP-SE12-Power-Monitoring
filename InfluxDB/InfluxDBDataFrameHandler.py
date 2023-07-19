import pandas as pd

class InfluxDBDataFrameHandler:
    def __init__(self):
        pass

    def format_as_dataframe(self, query_result) -> pd.DataFrame:
        """
        Converts Flux query results into a DataFrame for easier manipulation.

        Args:
            query_result: The query result object from InfluxDB.

        Returns:
            pd.DataFrame: The formatted DataFrame.
        """
        data = []
        exclude_keys = ['result', 'table', '_start', '_stop']
        for table in query_result:
            for record in table.records:
                record_dict = record.values  # Access the record values
                filtered_record = {k: v for k, v in record_dict.items() if k not in exclude_keys}
                data.append(filtered_record)
        return pd.DataFrame(data)
    
    def export_as_csv(self, dataframe, output_path):
        """
        Exports DataFrame to a CSV file.

        Args:
            dataframe: The DataFrame to export.
            output_path: The path to save the CSV file.
        """
        if dataframe.empty:
            raise ValueError("Dataframe is empty.")
        dataframe.to_csv(output_path, index=False)

    def get_value_and_formatted_time(self, dataframe) -> list:
        """
        Extracts the value, time, and measurement name from dataframe into a list.
        Args:
            dataframe: the dataframe to extract from.alerts
        Retruns:
            list: list containing values
        """
        if dataframe.empty:
            raise ValueError("Dataframe is empty.")

        df = dataframe[["_value", "_time", "_measurement"]]
        df_list = df.values.tolist()
        return df_list
    
    def load_from_csv(self, file_path) -> pd.DataFrame:
        """
        Loads a DataFrame from a CSV file.

        Args:
            file_path: The path to the CSV file.

        Returns:
            pd.DataFrame: The loaded DataFrame.
        """
        try:
            df = pd.read_csv(file_path)
            return df
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found at {file_path}.")
    
    def get_unique_values(self, df, column_name):
        """
        Extracts unique values from a specified column in a DataFrame.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data.
            column_name (str): The name of the column to extract unique values from.

        Returns:
            list: A list of unique values from the specified column.
        """
        unique_values = df[column_name].unique()
        return unique_values.tolist()
    
    def get_measurements_in_bucket(self, dataframe):
        measurements = dataframe["_measurement"].unique()
        return measurements
    
    def get_slice(self, df, column_name):
        return df[column_name]
    