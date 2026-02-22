from sqlalchemy.ext.declarative import declarative_base

DeclareModel = declarative_base()


class Base(DeclareModel):
    __abstract__ = True
