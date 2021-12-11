from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings.main import settings

engine = create_engine(settings.POSTGRES_DSN, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
