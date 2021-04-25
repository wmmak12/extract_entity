import sqlalchemy


def create_sqlite_engine(sqlite_db_path: str = 'gic.db'):
    # Instantiate the sqlite engine
    sqlEngine = sqlalchemy.create_engine(f"sqlite:///{sqlite_db_path}")
    return sqlEngine

