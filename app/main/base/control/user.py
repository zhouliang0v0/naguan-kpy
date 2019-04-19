# -*- coding:utf-8 -*-
from app.main.base.db import user as db_user


# 获取用户列表
def user_list(options=None):
    return db_user.user_list(options)


# 创建用户信息
def user_create(options=None):
    # 判断是否已存在用户名相同的用户
    user = db_user.user_list_by_name(options['username'])
    if not user:
        # 判断是否已存在用户名相同的用户
        email = db_user.user_list_by_name(options['email'])
        if not email == 0:
            return db_user.user_create(options)
        else:
            return False
    else:
        return False


# 删除用户信息
def user_delete(id=None):
    # 判断是否有用户
    user = db_user.user_list_by_id(id)
    if user:
        return db_user.user_delete(id)
    else:
        return False


# 更新用户信息
def user_update(id, options=None):
    # 判断是否有用户
    # print('update user')
    user = db_user.user_list_by_id(id)
    if user:
        # print('has user')
        # 更新用户信息
        return db_user.user_update(id, options)
    else:
        return False
