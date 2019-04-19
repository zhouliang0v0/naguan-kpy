# -*- coding:utf-8 -*-

from app.main.base.db import roles_users as db_role_user
from flask_security import SQLAlchemyUserDatastore, Security
from app.models import Users, Roles
from app.main.base.control.user import user_list_by_id
from app.main.base.control.role import role_list_by_id
from app.exts import db

user_datastore = SQLAlchemyUserDatastore(db, Users, Roles)


def security_init(app):
    Security(app, user_datastore)


def role_user_list(user_name, role_name):
    data = db_role_user.roles_users_list(user_name, role_name)
    user_role_list = []
    if data:

        for user_role in data:
            user_role_tmp = dict()

            user_role_tmp['user_id'] = user_role.user_id
            user_role_tmp['user_name'] = user_role.user_name
            user_role_tmp['role_id'] = user_role.role_id
            user_role_tmp['role_name'] = user_role.role_name
            user_role_list.append(user_role_tmp)

    return user_role_list


def role_user_update(user_id, new_role_id, old_role_id):

    user_info = user_list_by_id(user_id)
    new_role_info = role_list_by_id(new_role_id)
    old_role_info = role_list_by_id(old_role_id)

    user_datastore.remove_role_from_user(user_info.email, old_role_info.name)
    user_datastore.add_role_to_user(user_info.email, new_role_info.name)


def role_user_add(user_id, role_id):

    user_info = user_list_by_id(user_id)
    role_info = role_list_by_id(role_id)
    # print(user_info.email)
    # print(role_info.name)

    user_datastore.add_role_to_user(user_info.email, role_info.name)


def role_user_delete(user_id):
    user_info = user_list_by_id(user_id)

    role_list = db_role_user.role_user_list_by_id(user_id)
    if role_list:
        for role in role_list:
            role_info = role_list_by_id(role.role_id)
            user_datastore.remove_role_from_user(user_info.email, role_info.name)
    user_datastore.add_role_to_user(user_info.email, 'user')
    # 根据用户id查询所有角色信息