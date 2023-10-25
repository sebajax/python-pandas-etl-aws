# module import
import pandas as pd
from dataclasses import dataclass
from pandera.errors import SchemaErrors
import logging
# response import
from response_service import ResponseService
# schema import
from processor_schema import BatchProcessSchema, ValidationError
# db import
from db import ok_data_collection, error_data_collection
# get root logger
logger = logging.getLogger(__name__)


@dataclass
class BatchProcessService:
    """
    class to represent the batch process
    """
    file: str


    def __validate(self, data: dict) -> pd.Series | None:
        # validate process
        try:
            BatchProcessSchema(**data)
            return None
        except ValidationError as e:
            print(str(e))
            return pd.Series({**data, "Error": str(e)})

    def process(self) -> ResponseService:
        """
        use case resolution for processing and executing the batch data
        :return: process complete
        :rtype: ResponseService
        """
        # read excel and transform into a data frame
        df = pd.read_excel(self.file, na_filter=False)
        # remove unnamed columns & transform all elements to string
        df = df[df.filter(regex='^(?!Unnamed)').columns].map(str)

        # generate data frame with errors using head columns from process dataframe
        error_columns = df.columns.values.tolist()
        error_columns.append("Error")
        df_error = pd.DataFrame(columns=error_columns)

        # iterate through the DataFrame and validate each row
        for index, row in df.iterrows():
            validate = self.__validate(row.to_dict())
            if validate is not None:
                # only if we have errors
                df_error.loc[len(df_error)] = validate
                # remove the data from the dataframe
                df = df.drop(index)

        # insert errors if we have any
        if len(df_error) > 0:
            # df_error['Date'] = pd.to_datetime(df_error['Date'])
            df_error.to_dict('records')
            error_data_collection.insert_many(df_error.to_dict('records'))
            df_error.to_excel("errors.xlsx", index=False)

        # insert correct ones if we have any
        if len(df) > 0:
            df.to_dict('records')
            ok_data_collection.insert_many(df.to_dict('records'))

        # df['json'] = df.apply(lambda x: x.to_json(), axis=1)

        # return process status
        return ResponseService(
            detail="PROCESS_COMPLETE",
            data={
                "processed": len(df),
                "errors": len(df_error)
            }
        )


