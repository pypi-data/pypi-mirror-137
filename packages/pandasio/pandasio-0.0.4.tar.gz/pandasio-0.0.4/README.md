# PandasIO

PandasIO reimplements pandas.DataFrame.to_sql and
pandas.read_sql_query with more control over the SQL side of things
such as adding support for primary and foreign keys as well
serializing extra columns to JSON.

```
pandasio.get_new_ids(table, col, con, count=1)
pandasio.to_sql(df, name, con, keycols=[], references={}, chunksize=4096, method="multi", basecols=None, **kw)
pandasio.read_sql_query(sql, con, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize = None)
```
