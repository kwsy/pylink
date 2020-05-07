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
    total_score = Column(INT, nullable=False)

class Csdn(BaseModel):
    __tablename__ = 'csdn'
    id = Column(BIGINT, nullable=False, primary_key=True, autoincrement=True)
    original = Column(INT, nullable=False)
    fans = Column(INT, nullable=False)
    enjoy = Column(INT, nullable=False)
    comment = Column(INT, nullable=False)
    access = Column(INT, nullable=False)
    grade = Column(INT, nullable=False)
    week_sort = Column(INT, nullable=False)
    score = Column(INT, nullable=False)
    sort = Column(INT, nullable=False)
    total_score = Column(INT, nullable=False)

class Zhihu(BaseModel):
    __tablename__ = 'zhihu'
    id = Column(BIGINT, nullable=False, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(100), nullable=False)
    publish_count = Column(INT, nullable=False)
    follow_count = Column(INT, nullable=False)
    total_score = Column(INT, nullable=False)


def add_object(model, info):
    session = DBSession()
    obj = model(**info)
    session.add(obj)
    session.commit()
    session.close()


def query_data(model):
    session = DBSession()
    return session.query(model).all()

def query(model):
    session = DBSession()
    # select * from casdn where score > 12500
    # datas = session.query(model).filter(model.score > 12500)
    datas = session.query(model).all()
    for data in datas:
        print(data.href, data.score)

    session.close()


def create_table(table):
    BaseModel.metadata.create_all(engine, tables=[table.__table__])

if __name__=="__main__":
    query(Csdn)