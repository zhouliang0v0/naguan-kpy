# -*- coding:utf-8 -*-
from exts import db
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from passlib.apps import custom_app_context as pwd_context
from config import config, UPLOAD_DIR, BASE_DIR

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from flask import current_app
from config import config
import os
import datetime


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)


# User class
class User(db.Model, UserMixin):
    # Our User has six fields: ID, email, password, active, confirmed_at and roles. The roles field represents a
    # many-to-many relationship using the roles_users table. Each user may have no role, one role, or multiple roles.
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)                                    # 用户id
    username = db.Column(db.String(100), nullable=False, unique=True)               # 用户名
    password = db.Column(db.String(128), nullable=False)                            # 密码
    first_name = db.Column(db.String(100), nullable=False)                          # first name
    email = db.Column(db.String(120), nullable=False, unique=True)                  # 邮箱
    uid = db.Column(db.String(20), nullable=False, default='')                      # uid
    mobile = db.Column(db.String(30), nullable=False)                               # 手机
    department = db.Column(db.String(255), nullable=False)                          # 部门
    job = db.Column(db.String(100), nullable=False)                                 # 工作
    location = db.Column(db.String(30), nullable=False)                             # 地点
    company = db.Column(db.String(100), nullable=False)                             # 公司
    sex = db.Column(db.String(3), nullable=False)                                   # 性别
    uac = db.Column(db.Integer, nullable=False)                                     # UAC
    active = db.Column(db.Boolean, nullable=False)                                  # 激活状态
    is_superuser = db.Column(db.Boolean, nullable=False)                            # 是否是超管
    remarks = db.Column(db.String(255))                                             # 备注
    date_created = db.Column(db.DateTime, nullable=False,
                             default=lambda: datetime.datetime.utcnow())            # 创建时间
    confirmed_at = db.Column(db.DateTime, nullable=False,
                             default=lambda: datetime.datetime.utcnow())            # 确认时间

    last_login_at = db.Column(db.DateTime, nullable=False,
                              default=lambda: datetime.datetime.utcnow())           # 上次登录时间
    current_login_at = db.Column(db.DateTime, nullable=False,
                                 default=lambda: datetime.datetime.utcnow())        # 当前登录时间
    last_login_ip = db.Column(db.String(45), nullable=False)                        # 上传登录IP
    current_login_ip = db.Column(db.String(45), nullable=False)                     # 当前登录IP
    login_count = db.Column(db.Integer, nullable=False)                             # 登录次数

    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


# 系统配置
class SystemConfig(db.Model):
    __table_name__ = 'system_config'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #  平台名称
    platform_name = db.Column(db.String(32), unique=True)
    # 版本信息
    version_information = db.Column(db.String(32), unique=True)

    logo = db.Column(db.String(128), default=UPLOAD_DIR + 'iphone.png')
    # 版权
    copyright = db.Column(db.String(32), unique=True)
    # 用户验证模式
    user_authentication_mode = db.Column(db.String(16))
    # 是否开启调试模式
    debug = db.Column(db.Boolean, default=False)
    # 日志存储
    store_log = db.Column(db.String(100), default=BASE_DIR + 'app\\static\\store.log')
    ##


class Menu(db.Model):

    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)                    # 菜单项id
    ico = db.Column(db.String(20), default='')                                          # 图标
    url = db.Column(db.String(128), nullable=False)                                     # url
    name = db.Column(db.String(128), nullable=False)                                    # 名称
    identifier = db.Column(db.String(20), default='')                                   # 标识
    id_hide = db.Column(db.Boolean, default=False)                                      # 时候隐藏
    is_hide_children = db.Column(db.Boolean, default=False)                             # 是否隐藏子菜单
    important = db.Column(db.String(20), default=None)                                  # 重要
    parent_id = db.Column(db.Integer, default=0)                                        # 父菜单id
