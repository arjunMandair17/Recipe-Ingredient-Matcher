import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.db_models import Base

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}"
    f"/{os.getenv('POSTGRES_DB')}"
)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def init_db() -> None:
    """Create all tables defined in db_models if they do not already exist."""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Yield a DB session and close it afterward."""
    session = Session()
    try:
        yield session
    finally:
        session.close()


if __name__ == "__main__":
    init_db()
    print("Tables created.")
