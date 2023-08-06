"""Classes for all functionality within mssql_dataframe in a convenient package."""
import warnings
from importlib.metadata import version
import sys

from mssql_dataframe.connect import connect
from mssql_dataframe.core import (
    custom_warnings,
    custom_errors,
    conversion,
    create,
    modify,
    read,
)
from mssql_dataframe.core.write.write import write


class SQLServer(connect):
    """Class containing methods for creating, modifying, reading, and writing between dataframes and SQL Server.

    If autoadjust_sql_objects is True SQL objects may be modified such as creating a table, adding a column,
    or increasing the size of a column. The exception is internal tracking metadata columns _time_insert and
     _time_update which will always be created if include_metadata_timestamps=True.

    Parameters
    ----------
    database (str, default='master') : name of database to connect to
    server (str, default='localhost') : name of server to connect to
    driver (str, default=None) : ODBC driver name to use, if not given is automatically determined
    username (str, default=None) : if not given, use Windows account credentials to connect
    password (str, default=None) : if not given, use Windows account credentials to connect
    include_metadata_timestamps (bool, default=False) : include metadata timestamps _time_insert & _time_update in server time for write operations
    autoadjust_sql_objects (bool, default=False) : create and modify SQL table and columns as needed if True

    Properties
    ----------
    create : methods for creating SQL tables objects
    modify : methods for modifying tables columns and primary keys
    read : methods for reading from SQL tables
    write : methods for inserting, updating, and merging records

    Example
    -------

    #### connect to a local host database, with the ability to automatically adjust SQL objects
    sql = SQLServer(autoadjust_sql_objects=True)

    #### connect to Azure SQL Server instance
    sql = SQLServer(server='<server>.database.windows.net', username='<username>', password='<password>')

    Debugging
    ---------
    self._conn (dict) : values actually used in the connection, possibly derived by the connection
    self._versions (dict) : version numbers of required packages and the SQL server
    """

    def __init__(
        self,
        database: str = "master",
        server: str = "localhost",
        driver: str = None,
        username: str = None,
        password: str = None,
        include_metadata_timestamps: bool = False,
        autoadjust_sql_objects: bool = False,
    ):

        connect.__init__(self, database, server, driver, username, password)

        # initialize mssql_dataframe functionality with shared connection
        self.exceptions = custom_errors
        self.create = create.create(self.connection, include_metadata_timestamps)
        self.modify = modify.modify(self.connection)
        self.read = read.read(self.connection)
        self.write = write(
            self.connection, include_metadata_timestamps, autoadjust_sql_objects
        )

        # issue warnings for automated functionality
        if include_metadata_timestamps:
            warnings.warn(
                "SQL write operations will include metadata _time_insert & time_update columns as include_metadata_timestamps=True",
                custom_warnings.SQLObjectAdjustment,
            )

        if autoadjust_sql_objects:
            warnings.warn(
                "SQL objects will be created/modified as needed as autoadjust_sql_objects=True",
                custom_warnings.SQLObjectAdjustment,
            )

    def output_debug(self):
        """Generate useful debugging info to stdout. Includes connection info along with versions for Python, SQL, and required packages."""

        # determine versions for debugging
        self._versions = {}
        # Python
        self._versions["python"] = sys.version_info
        # SQL
        cur = self.connection.cursor()
        name = cur.execute("SELECT @@VERSION").fetchone()
        self._versions["sql"] = name[0]
        # packages
        names = ["mssql-dataframe", "pyodbc", "pandas"]
        for name in names:
            self._versions[name] = version(name)

        # output actual connection info (possibly derived within connection object)
        sys.stdout.write("Connection: \n" + str(self._conn) + "\n")
        # output Python/SQL/package versions
        sys.stdout.write("Versions: \n" + str(self._versions) + "\n")

    def get_schema(self, table_name: str):
        """Get schema of an SQL table and the defined conversion rules between data types.

        Parameters
        ----------
        table_name (str) : table name to read schema from

        Returns
        -------
        schema (pandas.DataFrame) : table column specifications and conversion rules
        """

        schema, _ = conversion.get_schema(self.connection, table_name)

        return schema
