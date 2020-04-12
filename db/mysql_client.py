from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, func, text, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy.types import *
from conf.mysql_conf import hjf_mysql_setting
import datetime
import time

connection_string = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}?charset={charset}"
connection_string = connection_string.format(**hjf_mysql_setting)
BaseModel = declarative_base()  # 创建对象的基类
engine = create_engine(connection_string, echo=False, pool_recycle=21600,
                       pool_size=5)  # pool_recycle多久之后对线程池中的线程进行一次连接的回收（重置） pool_size 连接池大小
DBSession = sessionmaker(bind=engine)


class PyWebsite(BaseModel):
    """
    配置mysql的pywebsite_hjf
    字段说明：
    mongo实例：
    {'score': 86, 'href': 'https://www.runoob.com/python3/python3-tutorial.html', 'insert_time': datetime.datetime(2020, 4, 11, 23, 3, 52, 52809)}
    """
    __tablename__ = 'pywebsite_hjf'
    id = Column(BIGINT, nullable=False, primary_key=True, autoincrement=True)
    href = Column(VARCHAR(100), nullable=False)
    score = Column(INT, nullable=False)
    web_rank = Column(INT, nullable=False)
    insert_time = Column(VARCHAR(50), nullable=False)


class Zhihu_hjf(BaseModel):
    """
    配置mysql的zhihu_hjf
    字段解释：
     {'id':ID唯一自增,'zhuanlan_name':专栏名称, 'follower':关注人数, 'original':原创, 'article_num':文章篇数,'zhuanlan_html':专栏url,'insert_time':插入时间}
     mongo实例：
     'zhuanlan_html':专栏url,'insert_time': 插入时间}
     {'href': 'https://www.zhihu.com/people/qin-lu-17/columns',
     'info': [{'zhuanlan_name': '运营大湿兄', 'follower': '26,859',
     'article_num': '42', 'zhuanlan_html': 'https://zhuanlan.zhihu.com/qinlu?author=qin-lu-17'}],
     'insert_time': datetime.datetime(2020, 4, 11, 22, 58, 18, 974100)}
    """
    __tablename__ = 'zhihu_hjf'
    id = Column(BIGINT, nullable=False, primary_key=True, autoincrement=True)
    href = Column(VARCHAR(100), nullable=False)
    zhuanlan_name = Column(VARCHAR(30), nullable=False)
    follower = Column(INT, nullable=False)
    article_num = Column(INT, nullable=False)
    zhuanlan_html = Column(VARCHAR(100), nullable=False)
    insert_time = Column(VARCHAR(50), nullable=False)


class Csdn_hjf(BaseModel):
    """
    配置mysql——csdn_hjf
    字段解释：
    {'id':ID唯一自增,'week_rank':周排名, 'sum_rank':总排名, 'original':原创, 'fans_num':粉丝,
     'like_num':获赞, 'comment_num':评论,'visit_num':访客, 'blog_level':博客等级, 'href':博主个人url，'insert_time': 插入时间}
    """
    __tablename__ = 'csdn_hjf'
    id = Column(BIGINT, nullable=False, primary_key=True, autoincrement=True)
    href = Column(VARCHAR(100), nullable=False)
    week_rank = Column(INT, nullable=False)
    sum_rank = Column(INT, nullable=False)
    original = Column(INT, nullable=False)
    fans_num = Column(INT, nullable=False)
    like_num = Column(INT, nullable=False)
    comment_num = Column(INT, nullable=False)
    visit_num = Column(INT, nullable=False)
    blog_level = Column(INT, nullable=False)
    insert_time = Column(VARCHAR(50), nullable=False)


def add_object(model, info):
    """
    执行添加ORM操作
    :param model:表类
    :param info: 添加列
    :return:
    """
    session = DBSession()
    obj = model(**info)
    session.add(obj)  # 添加一个对象
    session.commit()  # 提交事务
    session.close()  # 闭session，其实是将连接放回连接池


def update_object(model, info):
    """
    执行更新ORM操作
    :param model:
    :param info:
    :return:
    """
    session = DBSession()
    it_exists = session.query(exists().where(model.href == info['href'])).scalar()
    if not it_exists:
        add_object(model, info)
    else:
        session.query(model).filter(model.href == info['href']).update(info)
        session.commit()
        session.close()  # 闭session，其实是将连接放回连接池


def update_object_zhihu(model, info):
    """
    执行更新ORM操作
    :param model:
    :param info:
    :return:
    """
    session = DBSession()
    it_exists = session.query(exists().where(model.zhuanlan_html == info['zhuanlan_html'])).scalar()
    if not it_exists:
        add_object(model, info)
    else:
        session.query(model).filter(model.zhuanlan_html == info['zhuanlan_html']).update(info)
        session.commit()
        session.close()  # 闭session，其实是将连接放回连接池


def test():
    session = DBSession()  # 创建DBSession类型
    datas = session.query(Csdn_hjf).all()
    for data in datas:
        print(data.href, data.insert_time)


def test2():
    info = {'week_rank': '13938', 'sum_rank': '9432', 'original': '155', 'fans_num': '85', 'like_num': '42',
            'comment_num': '54', 'visit_num': '453570', 'blog_level': '6', 'href': 'https://me.csdn.net/KWSY2008',
            'insert_time': datetime.datetime(2020, 4, 12, 12, 6, 57, 279460)}
    info['insert_time'] = info['insert_time'].strftime("%Y-%m-%d")
    print(info['insert_time'])
    model = Csdn_hjf
    add_object(model, info)


def test3():
    info = {'week_rank': '13938', 'sum_rank': '9433', 'original': '155', 'fans_num': '85', 'like_num': '42',
            'comment_num': '54', 'visit_num': '453570', 'blog_level': '6', 'href': 'https://me.csdn.net/KWSY2008',
            'insert_time': datetime.datetime(2020, 4, 12, 12, 6, 57, 279460)}
    info['insert_time'] = info['insert_time'].strftime("%Y-%m-%d")
    print(info['insert_time'])
    model = Csdn_hjf
    update_object(model, info)


if __name__ == "__main__":
    test3()
    # test2()
