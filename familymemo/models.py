# -*- coding: utf-8 -*-
import datetime
from pyramid.security import (
    Allow,
    Everyone,
    )
class RootFactory(object):
    __acl__=[(Allow, Everyone, 'view'),
             (Allow, 'group:editors','edit') ]
    def __init__(self,request):
        pass
    

from sqlalchemy import (
    Column,
    Index,
    String,
    Integer,
    Text,
    Unicode,     #<- will provide unicode field,
    UnicodeText, #<- will provide unicode text field,
    DateTime,     #<- time abstraction field,
    Table,
    ForeignKey
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref
    )

from zope.sqlalchemy import ZopeTransactionExtension
#利用  scoped_session 全局访问数据库
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login_name = Column(Unicode(50), unique=True)
    nickname = Column(Unicode(50))
    password=Column(Unicode(50))
    tasks = relationship("Task", backref='user',
                cascade='all,delete,delete-orphan')
                        
    def __repr__(self):
        return('id:%r, login_name:%r'%(self.id, self.login_name))
        
    @classmethod
    def all(cls):
        return DBSession.query(User).all()
    

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    content = Column(String)
    owner = Column(Integer, ForeignKey('users.id'))
    status = Column(Integer) 
    edited = Column(DateTime, default=datetime.datetime.utcnow)
    def __repr__(self):
        return('Taskid:%r, content:%r'%(self.id, self.content))
    def brief_content(self):
        # 笨重的算法， 处理在首页显示开头若干长度的字符串，以适应列表的宽度
        # 因为英文显示所需的宽度小于 中文字符的宽度（约一半）
        fix_length=35       #头35个字符 （中文就是35个字符 ）
        count=0
        char_count=0
        if len(self.content) < fix_length :
            return self.content
        for c in self.content:
            char_count=char_count+1
            # to check the c is ASCII or others (like chinese)
            if ord(c) < 128 :
                count=count+0.45
            else :
                count=count+1
            if count > fix_length:
                break
        return self.content[:char_count]+'...'        
    
    @classmethod
    def all(cls):
        return DBSession.query(Task).all()
    @classmethod
    def all_active_task(cls):
        return DBSession.query(Task).filter(Task.status==0).all()

