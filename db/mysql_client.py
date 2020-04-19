from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, func, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy.types import *
from conf.mysql_conf import mysql_setting

connection_string = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}?charset=utf8"
connection_string = connection_string.format(**mysql_setting)
BaseModel = declarative_base()
engine = create_engine(connection_string, echo=False, pool_recycle=21600, pool_size=5)
DBSession = sessionmaker(bind=engine)


class PyWebsite(BaseModel):
    __tablename__ = 'py_website'
    id = Column(BIGINT, nullable=False, primary_key=True, autoincrement=True)
    href = Column(VARCHAR(100), nullable=False)
    score = Column(INT, nullable=False)


class Zhihu(BaseModel):
    __tablename__ = 'zhihu'
    id = Column(BIGINT, nullable=False, primary_key=True, autoincrement=True)
    href = Column(VARCHAR(100), nullable=False)
    name = Column(VARCHAR(30), nullable=False)
    score = Column(Float, nullable=False)


class Csdn(BaseModel):
    __tablename__ = 'csdn'
    id = Column(BIGINT, nullable=False, primary_key=True, autoincrement=True)
    href = Column(VARCHAR(100), nullable=False)
    score = Column(INT, nullable=False)

def add_object(model, info):
    session = DBSession()
    obj = model(**info)
    session.add(obj)
    session.commit()
    session.close()


def test():
    session = DBSession()
    datas = session.query(PyWebsite).all()
    for data in datas:
        print(data.href, data.score)


def create_table(table):
    BaseModel.metadata.create_all(engine, tables=[table.__table__])


if __name__ == '__main__':
    create_table(Csdn)