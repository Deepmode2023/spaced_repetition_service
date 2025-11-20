from sqlalchemy.ext.declarative import declarative_base
from collections import namedtuple


ClassArgument = namedtuple("ClassArgument", ["field", "nullable"])

DeclareModel = declarative_base()


class Base(DeclareModel):
    __abstract__ = True
