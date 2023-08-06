class SqlQuery:
    def __init__(self, query, columns: list, keyword: str):
        self.query: str = query
        self.columns: list = columns
        self.keyword: str = keyword
