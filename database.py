from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:05045313@localhost/test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Each instance of the SessionLocal class will be a database session. 
# The class itself is not a database session yet.
# But once we create an instance of the SessionLocal class, 
# this instance will be the actual database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declarative_base() returns a class. Inherit from this class 
# to create each of the database models or classes (the ORM models)
Base = declarative_base()