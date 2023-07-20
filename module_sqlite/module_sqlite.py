import sqlite3
from sqlite3 import Connection, Cursor, connect
from abc import ABC, abstractmethod


class DB_table(ABC):
    """
For ease of interaction with the database, given the task at hand, a slightly strange way of interaction is chosen,
which relies on the table entity rather than the entire database.
It is convenient only in examples without strong interaction between tables,
because all simplicity will turn into confusion
    """
    __sql_create_code: str
    __sql_check_exist: str
    __table_name: str

    @abstractmethod
    def __init__(self):
        pass

    def set_table_name(self, name: str):
        self.__table_name = name

    @abstractmethod
    def create(self, connection: Connection, cursor: Cursor) -> None:
        try:

            cursor.execute(self.__sql_create_code)
            connection.commit()

        except sqlite3.Error as e:
            print(f'Error in DB table creation {e}')

    @abstractmethod
    def set_sql_create_code(self, sql_create_code: str) -> None:
        self.__sql_create_code = sql_create_code

    @abstractmethod
    def check_table_exists(self, connection: Connection, cursor: Cursor) -> bool | None:
        try:
            cursor.execute(f'''SELECT name FROM sqlite_master WHERE type='table' AND name='{self.__table_name}';''')
            results = cursor.fetchall()
        except sqlite3.Error as e:
            print(f'Error in DB table check exists {e}')
        else:
            return len(results) > 0


class Table_Cookie_Profile(DB_table):
    def __init__(self):
        super().__init__()
        super().set_table_name("Cookie_Profile")

    def create(self, connection: Connection, cursor: Cursor) -> None:
        """Create table with those columns
            ID - FQDN
            datetime_create - not null date and time of record creation
            cookie_val - JSON cookies from this site
            datetime_execute - date, time of last execution
            amount_exec - number of executions
        """

        self.set_sql_create_code("""
            CREATE TABLE Cookie_Profile (
            id TEXT PRIMARY KEY,
            datetime_create DATETIME DEFAULT CURRENT_TIMESTAMP,
            cookie_val TEXT NULL,
            datetime_execute DATETIME NULL,
            amount_exec INT DEFAULT 0)
        """)
        return super().create(connection, cursor)

    def check_table_exists(self, connection: Connection, cursor: Cursor) -> bool | None:
        return super().check_table_exists(connection, cursor)

    def set_sql_create_code(self, sql_create_code: str) -> None:
        return super().set_sql_create_code(sql_create_code)

    def update_profile(self, connection: Connection, cursor: Cursor, params: tuple):
        url, cookie, datetime = params

        pass

class Database:
    __connection: Connection
    __cursor: Cursor

    def get_connection_cursor(self):
        return self.__connection, self.__cursor

    def __init__(self, fullpath: str):
        try:
            self.__connection = connect(fullpath)
            self.__cursor = self.__connection.cursor()
        except sqlite3.Error as e:
            print(f'Error in DB creation {e}')

    def table_exist(self, table: DB_table):
        return table.check_table_exists(self.__connection, self.__cursor)

    def create_table(self, table: DB_table):
        table.create(self.__connection, self.__cursor)
