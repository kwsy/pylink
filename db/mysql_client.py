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


def query_data(model):
    session = DBSession()
    return session.query(model).order_by(model.score).all()


def query(model):
    session = DBSession()
    # select * from csdn where score > 12500
    # datas = session.query(model).filter(model.score > 12500)
    datas = session.query(model).order_by(model.score).all()
    for data in datas:
        print(data.href, data.score)

    session.close()

def query_data_by_page(model, page=1, count=10):
    session = DBSession()
    datas = session.query(model).order_by(model.score)
    page_data = datas.limit(count).offset((page-1)*count)
    page_count = datas.count()//count + 1
    return page_data, page_count

def create_table(table):
    BaseModel.metadata.create_all(engine, tables=[table.__table__])


def clear():
    session = DBSession()
    sql = "delete from {table}"
    tables = ['py_website', 'zhihu', 'csdn']
    for table in tables:
        del_sql = sql.format(table=table)
        session.execute(del_sql)

    session.commit()

if __name__ == '__main__':
    clear()