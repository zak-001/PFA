from sqlalchemy import create_engine, MetaData

# SQLAlchemy connection to MySQL using mysqlclient
engine = create_engine(
    "mysql+mysqldb://root:root@db/flask_db",  # change credentials as needed
    pool_size=10,
    max_overflow=5,
    pool_recycle=280,
    echo=False  # set to True to see SQL output for debugging
)

# Metadata stores schema definitions
metadata = MetaData()
