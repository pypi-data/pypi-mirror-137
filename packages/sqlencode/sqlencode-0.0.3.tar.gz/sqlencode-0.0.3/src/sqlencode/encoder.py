import pandas as pd
from src.sqlencode.onehotsql import SqlQuery


def single_col_query(encoding_dataframe, col, col_prefix, sql_table):

    column_list = []
    big_query = ""
    query: list = [f"SELECT \"{encoding_dataframe.index.name}\",\n"]
    for cat in encoding_dataframe[col].unique()[:-1]:
        query.append(f"COUNT(CASE WHEN \"{col}\" = '{cat}' THEN 1 END) AS {col_prefix}{col}_{cat},\n")
        column_list.append(f"{col_prefix}{col}_{cat}")
    # Add last line without comma
    query.append(
        f"COUNT(CASE WHEN \"{col}\" = '{encoding_dataframe[col].unique()[-1]}' THEN 1 END) AS {col_prefix}{col}_{encoding_dataframe[col].unique()[-1]}\n")
    # add tail to sql
    column_list.append(f"{col_prefix}{col}_{encoding_dataframe[col].unique()[-1]}")
    query.append(f"from {sql_table}\n")
    query.append(f"group by \"{encoding_dataframe.index.name}\"")
    # Aggregate SQL
    for st in query:
        big_query = big_query + st
    sql_query = SqlQuery(big_query,column_list,encoding_dataframe.index.name)
    return sql_query


def combine_queries(query1: SqlQuery, query2: SqlQuery, table_index: int):
    table_index=table_index
    table1_columns = [f"id{str(table_index)}_t1." + x for x in query1.columns]
    table2_columns = [f"id{str(table_index)}_t2." + x for x in query2.columns]

    qbuilder = f"select id{str(table_index)}_t1.\"{query1.keyword}\", "
    for col in table1_columns + table2_columns:
        qbuilder = qbuilder + f"{col}, "

    #TODO make this into a SqlQuery object with nq.cols = q1.cols + q2.cols, keyword
    new_query = qbuilder[:-2]+f"\nFROM\n({query1.query}) as id{str(table_index)}_t1,\n({query2.query}) as id{str(table_index)}_t2"\
        + f"\nwhere id{str(table_index)}_t1.\"{query1.keyword}\"=id{str(table_index)}_t2.\"{query1.keyword}\""
    # print(table2_columns)
    return SqlQuery(new_query, query1.columns+query2.columns, query1.keyword) #return the object


class CategoricalEncoder:
    """
    Categorical encoder for encoding categorical variables using one hot encoding. SQL DIALECT = POSTGRES
    """

    def __init__(self):
        self.sql_dialect = "postgres"

    # @staticmethod
    def encode_dataframe_string(self, encoding_dataframe: pd.DataFrame(), sql_table: str, col_prefix: str = "") -> SqlQuery:
        """
        This function takes categorical features in a pandas dataframe and returns the categorical string
        to one hot sqlencode them.

        Args:
            encoding_dataframe: the dataframe with only categorical feature columns
            sql_table: the table that the sql is intended to run on

        Returns: sql string to sqlencode on database.

        """
        all_queries = {}

        # Create each line in the encoding sql
        for idx, col in enumerate(encoding_dataframe.columns):
            all_queries[col] = single_col_query(encoding_dataframe, col, col_prefix, sql_table)

        #Pass the new query into this

        agg_query=all_queries[list(all_queries.keys())[0]]
        for idx, key in enumerate(list(all_queries.keys())[:-1]):
            # print(key)
            # print(list(all_queries.keys())[idx], " : ", idx)
            agg_query=combine_queries(agg_query, all_queries[list(all_queries.keys())[idx+1]], table_index=idx)
        return agg_query
