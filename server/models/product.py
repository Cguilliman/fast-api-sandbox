import sqlalchemy as models
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request


# TODO: Fix postgres link
SQLALCHEMY_DATABASE_URL = "postgresql://market:qweqweqwe@localhost/market"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db(request: Request):
    return request.state.db


class BaseModel(Base):
    id = models.Column(
        models.Integer, primary_key=True,
        index=True, unique=True
    )


class Product(BaseModel):
    title = models.Column(models.String)
    description = models.Column(models.String)
    preview = models.Column(models.String)
