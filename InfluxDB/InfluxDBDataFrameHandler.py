import pandas as pd

class InfluxDBDataFrameHandler:
    def __init__(self):
        pass

    def format_as_dataframe(self, query_result) -> pd.DataFrame:
        """
        Converts Flux query results into a dataframe for easier manipulation

        Args:
            query_result: The query result object from InfluxDB

        Returns:
            pd.DataFrame: The formatted dataframe
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
        Exports dataframe to a CSV file

        Args:
            dataframe: The dataframe to export
            output_path: The path to save the CSV file
        """
        if dataframe.empty:
            raise ValueError("Dataframe is empty")
        dataframe.to_csv(output_path, index=False)

    def get_value_and_formatted_time(self, dataframe) -> list:
        if dataframe.empty:
            raise ValueError("Dataframe is empty")

        df = dataframe[["_value", "_time", "_measurement"]]
        df_list = df.values.tolist()
        return df_list