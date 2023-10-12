"""
pandera schemas definition for process
"""
import datetime
from datetime import date

import pandera as pa
from pandera import Column, DataFrameSchema, Check, Index

from pydantic import BaseModel, Field, ValidationError

batch_process_schema = DataFrameSchema(
    {
        "Date": Column(pa.DateTime, nullable=False),
        "Customer": Column(pa.String, nullable=False),
        "Sales": Column(pa.Int, Check.greater_than_or_equal_to(0), nullable=False)
    },
    index=Index(int),
)


class BatchProcessSchema(BaseModel):
    Date: datetime.datetime
    Customer: str
    Sales: int = Field(ge=0)
