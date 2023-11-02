from pandas_schema import Schema, Column
from pandas_schema.validation import (
    InRangeValidation,
    LeadingWhitespaceValidation,
    TrailingWhitespaceValidation,
    DateFormatValidation
)

schema = Schema([
    Column('Date', [DateFormatValidation("%Y-%m-%d %H:%M:%S")]),
    Column('Customer', [LeadingWhitespaceValidation(), TrailingWhitespaceValidation()]),
    Column('Sales', [InRangeValidation(min_value=0)])
])
