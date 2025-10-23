"""
SQLAlchemy Async Database URL Creator
Supports async drivers for: PostgreSQL, MySQL, SQLite, Oracle, MSSQL, and more
"""

from typing import Dict, Optional
from urllib.parse import quote_plus


class SQLAlchemyDSNGenerator:
    """Create SQLAlchemy database URLs with async driver support."""
    
    @staticmethod
    def postgresql(
        username: str,
        password: str,
        host: str = "localhost",
        port: int = 5432,
        database: str = "postgres",
        driver: str = "asyncpg",
        **kwargs
    ) -> str:
        """
        Create PostgreSQL connection string with async drivers.
        
        Async Drivers:
        - asyncpg (default, recommended) - pure Python, fast
        - psycopg (psycopg3 with async support)
        - aiopg (legacy, based on psycopg2)
        
        Sync Drivers:
        - psycopg2
        - pg8000
        """
        pwd = quote_plus(password)
        url = f"postgresql+{driver}://{username}:{pwd}@{host}:{port}/{database}"
        
        if kwargs:
            params = "&".join([f"{k}={quote_plus(str(v))}" for k, v in kwargs.items()])
            url += f"?{params}"
        
        return url
    
    @staticmethod
    def mysql(
        username: str,
        password: str,
        host: str = "localhost",
        port: int = 3306,
        database: str = "mysql",
        driver: str = "aiomysql",
        charset: str = "utf8mb4",
        **kwargs
    ) -> str:
        """
        Create MySQL connection string with async drivers.
        
        Async Drivers:
        - aiomysql (default) - async MySQL client
        - asyncmy - pure Python async MySQL client
        
        Sync Drivers:
        - pymysql
        - mysqldb
        - mysqlconnector
        """
        pwd = quote_plus(password)
        params = {"charset": charset}
        params.update(kwargs)
        
        query_str = "&".join([f"{k}={quote_plus(str(v))}" for k, v in params.items()])
        return f"mysql+{driver}://{username}:{pwd}@{host}:{port}/{database}?{query_str}"
    
    @staticmethod
    def mariadb(
        username: str,
        password: str,
        host: str = "localhost",
        port: int = 3306,
        database: str = "mariadb",
        driver: str = "aiomysql",
        **kwargs
    ) -> str:
        """
        Create MariaDB connection string with async drivers.
        
        Async Drivers: aiomysql (default), asyncmy
        """
        pwd = quote_plus(password)
        url = f"mariadb+{driver}://{username}:{pwd}@{host}:{port}/{database}"
        
        if kwargs:
            params = "&".join([f"{k}={quote_plus(str(v))}" for k, v in kwargs.items()])
            url += f"?{params}"
        
        return url
    
    @staticmethod
    def sqlite(
        database: str = "database.db",
        memory: bool = False,
        driver: str = "aiosqlite"
    ) -> str:
        """
        Create SQLite connection string with async driver.
        
        Async Driver: aiosqlite (default)
        Sync Driver: pysqlite (omit driver param)
        
        Args:
            database: Path to database file
            memory: If True, creates in-memory database
            driver: Use 'aiosqlite' for async or None for sync
        """
        if memory:
            if driver:
                return f"sqlite+{driver}:///:memory:"
            return "sqlite:///:memory:"
        
        if driver:
            return f"sqlite+{driver}:///{database}"
        return f"sqlite:///{database}"
    
    @staticmethod
    def oracle(
        username: str,
        password: str,
        host: str = "localhost",
        port: int = 1521,
        service_name: Optional[str] = None,
        sid: Optional[str] = None,
        driver: str = "oracledb",
        async_mode: bool = True,
        **kwargs
    ) -> str:
        """
        Create Oracle connection string.
        
        Drivers:
        - oracledb (python-oracledb, supports async with async_mode=True)
        - cx_oracle (legacy, sync only)
        
        Either service_name or sid must be provided.
        """
        pwd = quote_plus(password)
        
        if service_name:
            dsn = f"{host}:{port}/?service_name={service_name}"
        elif sid:
            dsn = f"{host}:{port}/{sid}"
        else:
            raise ValueError("Either service_name or sid must be provided")
        
        url = f"oracle+{driver}://{username}:{pwd}@{dsn}"
        
        if async_mode and driver == "oracledb":
            kwargs["async_mode"] = "True"
        
        if kwargs:
            params = "&".join([f"{k}={quote_plus(str(v))}" for k, v in kwargs.items()])
            url += f"&{params}" if "?" in url else f"?{params}"
        
        return url
    
    @staticmethod
    def mssql(
        username: str,
        password: str,
        host: str = "localhost",
        port: int = 1433,
        database: str = "master",
        driver: str = "aioodbc",
        odbc_driver: str = "ODBC Driver 18 for SQL Server",
        trusted_connection: bool = False,
        encrypt: str = "yes",
        trust_server_certificate: str = "no",
        **kwargs
    ) -> str:
        """
        Create Microsoft SQL Server connection string with async drivers.
        
        Async Drivers:
        - aioodbc (default) - async ODBC driver
        
        Sync Drivers:
        - pyodbc
        - pymssql
        
        Note: aioodbc requires unixODBC (Linux/Mac) or ODBC Driver Manager (Windows)
        """
        pwd = quote_plus(password)
        
        if driver == "aioodbc" or driver == "pyodbc":
            driver_encoded = quote_plus(odbc_driver)
            params = {
                "driver": odbc_driver,
                "Encrypt": encrypt,
                "TrustServerCertificate": trust_server_certificate
            }
            params.update(kwargs)
            
            if trusted_connection:
                params["Trusted_Connection"] = "yes"
                url = f"mssql+{driver}://{host}:{port}/{database}"
            else:
                url = f"mssql+{driver}://{username}:{pwd}@{host}:{port}/{database}"
            
            query_str = "&".join([f"{k}={quote_plus(str(v))}" for k, v in params.items()])
            url += f"?{query_str}"
            
        elif driver == "pymssql":
            url = f"mssql+pymssql://{username}:{pwd}@{host}:{port}/{database}"
            if kwargs:
                params = "&".join([f"{k}={quote_plus(str(v))}" for k, v in kwargs.items()])
                url += f"?{params}"
        else:
            url = f"mssql+{driver}://{username}:{pwd}@{host}:{port}/{database}"
            if kwargs:
                params = "&".join([f"{k}={quote_plus(str(v))}" for k, v in kwargs.items()])
                url += f"?{params}"
        
        return url
    
    @staticmethod
    def cockroachdb(
        username: str,
        password: str,
        host: str = "localhost",
        port: int = 26257,
        database: str = "defaultdb",
        cluster: Optional[str] = None,
        driver: str = "asyncpg",
        sslmode: str = "require",
        **kwargs
    ) -> str:
        """
        Create CockroachDB connection string with async driver.
        
        Async Drivers: asyncpg (default), psycopg (async)
        Sync Drivers: psycopg2
        """
        pwd = quote_plus(password)
        params = {"sslmode": sslmode}
        params.update(kwargs)
        
        if cluster:
            url = f"cockroachdb+{driver}://{username}:{pwd}@{cluster}/{database}"
        else:
            url = f"cockroachdb+{driver}://{username}:{pwd}@{host}:{port}/{database}"
        
        query_str = "&".join([f"{k}={quote_plus(str(v))}" for k, v in params.items()])
        url += f"?{query_str}"
        
        return url
    
    @staticmethod
    def snowflake(
        username: str,
        password: str,
        account: str,
        database: str,
        schema: str = "public",
        warehouse: Optional[str] = None,
        role: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Create Snowflake connection string.
        
        Note: Snowflake connector supports async operations natively
        """
        pwd = quote_plus(password)
        url = f"snowflake://{username}:{pwd}@{account}/{database}/{schema}"
        
        params = {}
        if warehouse:
            params["warehouse"] = warehouse
        if role:
            params["role"] = role
        params.update(kwargs)
        
        if params:
            query_str = "&".join([f"{k}={quote_plus(str(v))}" for k, v in params.items()])
            url += f"?{query_str}"
        
        return url
    
    @staticmethod
    def redshift(
        username: str,
        password: str,
        host: str,
        port: int = 5439,
        database: str = "dev",
        driver: str = "asyncpg",
        **kwargs
    ) -> str:
        """
        Create Amazon Redshift connection string with async driver.
        
        Async Drivers: asyncpg (recommended), psycopg (async)
        Sync Drivers: psycopg2
        """
        pwd = quote_plus(password)
        url = f"redshift+{driver}://{username}:{pwd}@{host}:{port}/{database}"
        
        if kwargs:
            params = "&".join([f"{k}={quote_plus(str(v))}" for k, v in kwargs.items()])
            url += f"?{params}"
        
        return url
    
    @staticmethod
    def bigquery(
        project_id: str,
        dataset_id: Optional[str] = None,
        credentials_path: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Create Google BigQuery connection string.
        
        Note: Uses google-cloud-bigquery which has async support
        """
        url = f"bigquery://{project_id}"
        if dataset_id:
            url += f"/{dataset_id}"
        
        params = {}
        if credentials_path:
            params["credentials_path"] = credentials_path
        params.update(kwargs)
        
        if params:
            query_str = "&".join([f"{k}={quote_plus(str(v))}" for k, v in params.items()])
            url += f"?{query_str}"
        
        return url
    
    @staticmethod
    def custom(
        dialect: str,
        driver: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        query_params: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Create a custom connection string for any database.
        
        Example:
            custom("postgresql", "asyncpg", "user", "pass", "localhost", 5432, "mydb")
        """
        if driver:
            url = f"{dialect}+{driver}://"
        else:
            url = f"{dialect}://"
        
        if username and password:
            pwd = quote_plus(password)
            url += f"{username}:{pwd}@"
        elif username:
            url += f"{username}@"
        
        if host:
            url += host
            if port:
                url += f":{port}"
        
        if database:
            url += f"/{database}"
        
        if query_params:
            params = "&".join([f"{k}={quote_plus(str(v))}" for k, v in query_params.items()])
            url += f"?{params}"
        
        return url
