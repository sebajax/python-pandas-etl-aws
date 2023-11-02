# module import
import io
import logging
from dataclasses import dataclass

import pandas as pd
from pydantic import ValidationError

# infrastructure import
from infrastructure.bucket_infrastructure import BucketInfrastructure
from infrastructure.repository_infrastructure import RepositoryInfrastructure
# schema import
from schemas.processor_schema import BatchProcessSchema
from services.exception_service import ServiceException
# service import
from services.response_service import ResponseService

# get root logger
logger = logging.getLogger(__name__)


@dataclass
class BatchProcessService:
    """
    class to represent the batch process
    """
    file: str
    bucket_infrastructure: BucketInfrastructure
    repository_infrastructure: RepositoryInfrastructure

    @classmethod
    def __validate(cls, data: dict) -> pd.Series | None:
        # validate process
        try:
            BatchProcessSchema(**data)
            return None
        except ValidationError as e:
            logger.error("validation error %s", str(e))
            return pd.Series({**data, "Error": str(e)})

    @classmethod
    def __transform_data(cls, df_error: pd.DataFrame) -> bytes:
        # use the BytesIO object as the filehandle
        with io.BytesIO() as output:
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_error.to_excel(writer, index=False)
            xlsx_data = output.getvalue()

        return xlsx_data

    def process(self) -> ResponseService:
        """
        use case resolution for processing and executing the batch data
        :return: process complete
        :rtype: ResponseService
        """
        try:
            # get the Excel file in bytes
            data = self.bucket_infrastructure.get_file_from_bucket()
            if data is None:
                raise ServiceException(detail="DATA_SENT_IS_EMPTY")

            # read excel and transform into a data frame
            df = pd.read_excel(data, na_filter=False)
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
                (self.repository_infrastructure.error_data_collection()
                 .insert_many(df_error.to_dict('records')))
                # transform error data frame into byte array
                xlsx_data = self.__transform_data(df_error)
                # write excel into s3 bucket
                self.bucket_infrastructure.write_file_into_bucket(xlsx_data)

            # insert correct ones if we have any
            if len(df) > 0:
                df.to_dict('records')
                (self.repository_infrastructure.ok_data_collection()
                 .insert_many(df.to_dict('records')))

            # df['json'] = df.apply(lambda x: x.to_json(), axis=1)

            # return process status
            return ResponseService(
                detail="PROCESS_COMPLETE",
                data={
                    "processed": len(df),
                    "errors": len(df_error)
                }
            )

        except Exception as e:
            logger.error("process error %s", e)
            raise ServiceException(detail="PROCESS_ERROR")
