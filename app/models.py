# -*- coding:utf-8 -*-
from exts import db
from flask_security import Security, UserMixin, RoleMixin, login_required
from passlib.apps import custom_app_context as pwd_context
from config import config, UPLOAD_DIR, BASE_DIR
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
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
    id = db.Column(db.Integer, primary_key=True)  # 用户id
    username = db.Column(db.String(100), nullable=False, unique=True)  # 用户名
    password = db.Column(db.String(128), nullable=False)  # 密码
    first_name = db.Column(db.String(100), nullable=False)  # first name
    email = db.Column(db.String(120), nullable=False, unique=True)  # 邮箱
    uid = db.Column(db.String(20), nullable=False, default='')  # uid
    mobile = db.Column(db.String(30), nullable=False)  # 手机
    department = db.Column(db.String(255), nullable=False)  # 部门
    job = db.Column(db.String(100), nullable=False)  # 工作
    location = db.Column(db.String(30), nullable=False)  # 地点
    company = db.Column(db.String(100), nullable=False)  # 公司
    sex = db.Column(db.String(3), nullable=False)  # 性别
    uac = db.Column(db.Integer, nullable=False)  # UAC
    active = db.Column(db.Boolean, nullable=False)  # 激活状态
    is_superuser = db.Column(db.Boolean, nullable=False)  # 是否是超管
    remarks = db.Column(db.String(255))  # 备注
    date_created = db.Column(db.DateTime, nullable=False,
                             default=lambda: datetime.datetime.utcnow())  # 创建时间
    confirmed_at = db.Column(db.DateTime, nullable=False,
                             default=lambda: datetime.datetime.utcnow())  # 确认时间

    last_login_at = db.Column(db.DateTime, nullable=False,
                              default=lambda: datetime.datetime.utcnow())  # 上次登录时间
    current_login_at = db.Column(db.DateTime, nullable=False,
                                 default=lambda: datetime.datetime.utcnow())  # 当前登录时间
    last_login_ip = db.Column(db.String(45), nullable=False)  # 上传登录IP
    current_login_ip = db.Column(db.String(45), nullable=False)  # 当前登录IP
    login_count = db.Column(db.Integer, nullable=False)  # 登录次数

    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

        return s.dumps({'id': self.id, 'username': self.username})

    @staticmethod
    def get_hash_password(password):
        return pwd_context.encrypt(password)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            code = 1
        except SignatureExpired:
            data = ''
            code = 2
        except BadSignature:
            data = ''
            code = 3
        # user = User.query.get(data['id'])
        return data, code


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
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 菜单项id
    icon = db.Column(db.String(20), default='')  # 图标
    url = db.Column(db.String(128), nullable=False)  # url
    name = db.Column(db.String(128), nullable=False)  # 名称
    identifier = db.Column(db.String(20), default='')  # 标识
    is_hide = db.Column(db.Boolean, default=False)  # 时候隐藏
    is_hide_children = db.Column(db.Boolean, default=False)  # 是否隐藏子菜单
    important = db.Column(db.String(20), default=None)  # 重要
    parent_id = db.Column(db.Integer, default=0)  # 父菜单id
    date_created = db.Column(db.DateTime, nullable=True,
                             default=lambda: datetime.datetime.now())  # 创建时间


class RequestLog(db.Model):
    __tablename__ = 'request_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(db.String(100), nullable=False)  # 请求ID
    ip = db.Column(db.String(20), nullable=False)  # 请求ip
    url = db.Column(db.String(255), nullable=False)  # url（请求方法+api）
    status_num = db.Column(db.Integer)  # 状态值
    submitter = db.Column(db.String(32), nullable=False)  # 提交者
    time = db.Column(db.DateTime, default=datetime.datetime.now())  # 创建时间
    event_logs = db.relationship('EventLog', backref='request_logs', lazy=True)  # 关联表


class TaskLog(db.Model):
    __tablenname__ = 'task_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.String(100), nullable=False)  # 任务ID
    rely_task_id = db.Column(db.String(100))  # 依赖任务
    status = db.Column(db.String(10), nullable=False)  # 状态
    await_execute = db.Column(db.String(10), nullable=False)  # 等待/执行
    queue_name = db.Column(db.String(32), nullable=False)  # 队列名
    method_name = db.Column(db.String(32), nullable=False)  # 方法名
    submitter = db.Column(db.String(32), nullable=False)  # 提交者
    enqueue_time = db.Column(db.DateTime, default=datetime.datetime.now())  # 入队时间
    start_time = db.Column(db.DateTime)  # 开始时间
    end_time = db.Column(db.DateTime)  # 结束时间
    event_logs = db.relationship('EventLog', backref='task_logs', lazy=True)  # 关联表


class EventLog(db.Model):
    __tablename__ = 'event_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resource_type = db.Column(db.String(32), nullable=False)  # 操作资源类型
    result = db.Column(db.String(10))  # 操作结果
    operation_resources_id = db.Column(db.Integer, nullable=False)  # 操作资源ID
    operation_event = db.Column(db.String(255))  # 操作事件
    submitter = db.Column(db.String(32), nullable=False)  # 提交者
    time = db.Column(db.DateTime, default=datetime.datetime.now())  # 创建时间
    # 外键
    event_request_id = db.Column(db.String, db.ForeignKey(RequestLog.request_id))  # 请求ID
    task_request_id = db.Column(db.String, db.ForeignKey(TaskLog.task_id))  # 任务ID


class Instance(db.Model):
    __tablename__ = 'instances'
    id = db.Column(db.Integer, primary_key=True)
    int_id = db.Column(db.String(40), unique=True, nullable=False)
    group_id = db.Column(db.String(10), nullable=False, index=True)
    pool_id = db.Column(db.String(40), nullable=False, index=True)
    uuid = db.Column(db.String(40), nullable=False)
    sid = db.Column(db.String(30), nullable=False)
    ip = db.Column(db.String(20), nullable=False)
    vip = db.Column(db.String(20), nullable=False)
    port = db.Column(db.SmallInteger, nullable=False)
    domain = db.Column(db.String(100), nullable=False, index=True)
    role = db.Column(db.SmallInteger, nullable=False)
    dbtype = db.Column(db.String(10), nullable=False)
    maxmemory = db.Column(db.String(32), nullable=False)
    intcode = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.TIMESTAMP, nullable=False, default=0)
    down_time = db.Column(
        db.TIMESTAMP,
        nullable=False,
        default='0000-00-00 00:00:00'
    )
    status = db.Column(db.SmallInteger, nullable=False)
    version = db.Column(db.String(30), nullable=False)
    ins_usage = db.Column(db.String(120), nullable=False)
    proj_name = db.Column(db.String(20), nullable=False, default='')
    backup_flag = db.Column(db.SmallInteger, nullable=False, default=0)
    slow_flag = db.Column(db.SmallInteger, nullable=False, default=0)
    injection_flag = db.Column(db.SmallInteger, nullable=False, default=0)
    protect = db.Column(db.SmallInteger, nullable=False, default=0)
    sleep_prec = db.Column(db.SmallInteger, nullable=False, default=0)
    service_ip = db.Column(db.String(20), nullable=False, default='')
    offline_desc = db.Column(db.String(255), nullable=False, default='')

    def __repr__(self):
        return '<Instance %r>' % self.int_id

    def __unicode__(self):
        return self.int_id


class UsersInstances(db.Model):
    __tablename__ = 'user_insnstance'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    int_id = db.Column(db.String(40), nullable=False)

    # user = db.relationship('User', uselist=False, backref=db.backref('intids', lazy='dynamic'))
    # intid = db.relationship('Instance', uselist=False, backref=db.backref('intids', lazy='dynamic'))

    def __repr__(self):
        return '<UserID:%r / IntID:%r>' % (self.user_id, self.int_id)

    def __unicode__(self):
        return self.id


class CloudPlatformType(db.Model):
    __tablename__ = 'cloud_platform_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)


class CloudPlatform(db.Model):
    __tablename__ = 'cloud_platform'
    id = db.Column(db.Integer, primary_key=True)
    platform_type_id = db.Column(db.Integer, nullable=False)
    platform_name = db.Column(db.String(255), nullable=False, unique=True)
    ip = db.Column(db.String(30), nullable=False)
    port = db.Column(db.String(30))
    admin_name = db.Column(db.String(30), nullable=False)
    admin_password = db.Column(db.String(30), nullable=False)
    remarks = db.Column(db.String(255))  # 备注


class VCenterTree(db.Model):
    __tablename__ = 'vcenter_tree'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)    # 类型

    platform_id = db.Column(db.Integer, nullable=False, )  # platform_id
    dc_host_folder_mor_name = db.Column(db.String(255))
    dc_mor_name = db.Column(db.String(255))
    dc_oc_name = db.Column(db.String(255))
    dc_vm_folder_mor_name = db.Column(db.String(255))
    mor_name = db.Column(db.String(255))
    name = db.Column(db.String(255), nullable=False)
    cluster_mor_name = db.Column(db.String(255))
    cluster_oc_name = db.Column(db.String(255))


