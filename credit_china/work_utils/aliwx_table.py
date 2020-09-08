# -*- coding: utf-8 -*-
from datetime import datetime
import warnings

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from credit_china.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_NAME, MYSQL_CHARSET
from sqlalchemy import Column, Integer, String, TEXT, DATETIME, SMALLINT, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT

warnings.filterwarnings("ignore")
Base = declarative_base()
# 初始化数据库连接:
engine = create_engine(
    "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset={charset}".format(username=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOST, port=MYSQL_PORT, db=MYSQL_NAME, charset=MYSQL_CHARSET),
    # echo=True,  # 打印过程
    # max_overflow=0,  # 超过连接池大小外最多创建的连接
    # pool_size=5,  # 连接池大小
    # pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    # pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收(重置)
)


class AliWenxue(Base):
    """小说存储表"""
    __tablename__ = 'aliwx'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    book_name = Column(String(length=64), nullable=False, comment='书名')
    author_name = Column(String(length=32), nullable=True, index=True, comment='作者')
    volume_name = Column(String(length=64), nullable=False, comment='第几卷')
    chapter_name = Column(String(length=64), nullable=False, comment='章节名')
    content = Column(LONGTEXT, nullable=True, comment='章节内容')
    cp_name = Column(String(length=16), nullable=True, comment='是否原创')
    chapter_num = Column(Integer, nullable=True, comment='书总共章节数')
    img_url = Column(String(length=128), nullable=True, comment='封面图')
    word_count = Column(Integer, nullable=True, comment='总字数')
    any_uptime = Column(DATETIME, nullable=True, comment='开始更新时间')
    last_instime = Column(DATETIME, nullable=True, comment='最后一次更新时间')
    spider_time = Column(DATETIME, nullable=True, default=datetime.now, comment='抓取时间')
    chapter_word_count = Column(Integer, nullable=True, comment='章节总字数')
    url = Column(String(length=512), nullable=True, unique=True, comment='文章链接')  # url唯一用来去重

    def __repr__(self):
        return "<AliWenxue %r>" % self.book_name


if __name__ == '__main__':
    Base.metadata.create_all(engine)  # 新建表
    # Base.metadata.drop_all(engine)  # 删除表