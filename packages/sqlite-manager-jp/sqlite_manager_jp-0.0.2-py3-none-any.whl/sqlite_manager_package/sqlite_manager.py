"""
create a simple sqlite helper class to automatically commit 
by using the connection as a context manager, 
and reduce the amount of boilerplate codes when doing
sqlite query.
"""

import sqlite3
import pathlib
from typing import Any, Iterable, Tuple, List, Optional


from sqlite_manager_package.common_query import CommonQuery

class SqliteManager:
    """a class to execute basic sqlite queries"""
    def __init__(self, sqlite_db_path: str) -> None:
        if not self._is_valid_database(sqlite_db_path):
            raise ValueError(f'{sqlite_db_path} is not a valid database file.')
        self.database = sqlite_db_path
    
    def _is_valid_database(self, possible_db_path: str) -> bool:
        path = pathlib.Path(possible_db_path)
        if path.exists() and path.is_file() and path.suffix == '.db':
            return True
        return False
    
    def _is_select_query(self, sql: str) -> bool:
        return sql.split()[0].upper() == 'SELECT'
      
    def execute_query(self, sql: str, parameters: Optional[Iterable] = None) -> None:
        connection = sqlite3.connect(self.database)
        with connection:
            try:
                if parameters:
                    connection.execute(sql, parameters)
                else:
                    connection.execute(sql)
                print("Query successful")
            except sqlite3.Error as error:
                print(f'Error: {error}')
        connection.close()

    def excecute_many_queries(self, sql: str, many_parameters: Iterable) -> None:
        connection = sqlite3.connect(self.database)
        with connection:
            try: 
                connection.executemany(sql, many_parameters)
                print("Query successful")
            except sqlite3.Error as error:
                print(f'Error: {error}') 
        connection.close()
    
    def select_query(self, sql: str, parameters: Optional[Iterable] = None) -> List[Tuple[Any]]:
        assert self._is_select_query(sql)
        result = []
        connection = sqlite3.connect(self.database)
        with connection:
            cursor = connection.cursor()
            try: 
                if parameters:
                    cursor.execute(sql, parameters)
                else:
                    cursor.execute(sql)
                print("Query successful")
                result = cursor.fetchall()
            except sqlite3.Error as error:
                print(f'Error: {error}') 
        connection.close()
        return result

    def is_table_exist(self, table_name: str) -> bool:
        select_result = self.select_query(
            CommonQuery.select_count_table, (table_name,))
        table_count = select_result[0][0]
        return table_count > 0 

