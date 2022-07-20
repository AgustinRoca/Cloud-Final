import os

import sqlalchemy

def connect_replica() -> sqlalchemy.engine.base.Engine:
    os.environ['DB_USER'] =  'postgres'
    os.environ['DB_PASS'] =  'postgres'
    os.environ['DB_NAME'] =  'images'
    os.environ['INSTANCE_HOST'] =  '10.0.2.6'
    db_user = os.environ["DB_USER"]  # e.g. 'my-database-user'
    db_pass = os.environ["DB_PASS"]  # e.g. 'my-database-password'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'
    db_host = os.environ["INSTANCE_HOST"]
    db_port = 5432

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,
            password=db_pass,
            database=db_name,
            host=db_host,
            port=db_port,
        ),
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,  # 30 seconds
        pool_recycle=1800,  # 30 minutes
    )
    return pool