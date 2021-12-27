import datetime

from to_do_flask.db import db
from sqlalchemy import Column, Boolean, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from flask import Flask


association_table = Table('association', db.metadata,
                          Column('user_id', ForeignKey('user.id'), primary_key=True),
                          Column('task_id', ForeignKey('task.id'), primary_key=True),
                          extend_existing=True
                          )


class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    task = relationship('Task', secondary=association_table, back_populates='user')

    def __init__(self, username):
        self.username = username


class Task(db.Model):
    __tablename__ = "task"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String, nullable=False, unique=True)
    deadline = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    user = relationship('User', secondary=association_table, back_populates='task')

    def __init__(self, task, user, deadline=None):
        self.task = task
        self.deadline = deadline
        self.user = user


def create_tables(app: Flask):
    db.create_all(app=app)
