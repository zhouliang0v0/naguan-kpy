# -*- coding:utf-8 -*-
from app.main.base.db.role import role_list_db, role_create_db, role_update_db, role_exist, role_delete_db


# 角色列表
def role_list_c(options=None):
    if role_list_db(options):
        return role_list_db(options)
    else:
        return False


# 创建角色信息
def role_create_c(options=None):
    role = role_create_db(options)
    if role:
        return role
    else:
        return False


# 更新角色信息
def role_update_c(options=None):
    role = role_update_db(options)
    if role:
        return True
    else:
        return False


# 删除角色信息
def role_delete_c(id=None):
    try:
        name = role_delete_db(id)
        return name
    except Exception as e:
        return False
