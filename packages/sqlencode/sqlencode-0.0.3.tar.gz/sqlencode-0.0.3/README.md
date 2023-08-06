# sqlencode
A package to create strings to encode datasets using sql from pandas datasets.
This package is intended to be used when developing sql for large datasets based on encoding samples in pandas.

## Usage

```angular2html
from sqlencode.encoder import CategoricalEncoder
encoder = CategoricalEncoder()
query = encoder.encode_dataframe_string(df[["col1", "col2"]], sql_table="tablename")
```

## Limitations
Currently only one-hot encoding is supported. 
Currently only postgresql dialect is generated.

## Returns the SqlQuery Object
The SqLQuery class has 3 attributes: 

query: The query itself as a string

columns: The output list of columns, used to export columns for further manipulation

keyword: the keyword (index column name) 

## Future Releases
Some activities planned for this package in the near future:
1. Other encoding techniques (Dummy, Numerical/Mean, Ordinal etc.)
2. Other sql dialects (MySQL, NoSQL)
3. More sql functionality (create tables, views)
