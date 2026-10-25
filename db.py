import os
from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database URL configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("mysql+mysqldb://"):
    DATABASE_URL = DATABASE_URL.replace("mysql+mysqldb://", "mysql+pymysql://")
    if "?" in DATABASE_URL:
        # PyMySQL expects different SSL parameters than MySQLdb
        base_url = DATABASE_URL.split("?")[0]
        DATABASE_URL = base_url + "?ssl_verify_cert=true&ssl_verify_identity=true"

if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./placement_pilot.db"

# Create database engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# Create base class for models
Base = declarative_base()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()