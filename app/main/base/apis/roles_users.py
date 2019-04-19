# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse

from app.common.tool import set_return_val
from app.main.base.control import roles_users as role_user_manage

parser = reqparse.RequestParser()
parser.add_argument('user_id')
parser.add_argument('role_id')
parser.add_argument('new_role_id')
parser.add_argument('old_role_id')

parser.add_argument('role_name', type=str)
parser.add_argument('user_name', type=str)


class RolesUsersManage(Resource):
    def get(self):
        try:
            args = parser.parse_args()
            user_name = args.get('user_name')
            role_name = args.get('role_name')
            # 获取所有用户角色权限 列表
            data = role_user_manage.role_user_list(user_name, role_name)
        except Exception as e:
            return set_return_val(False, {}, str(e), 1234), 400
        return set_return_val(True, data, '获取列表成功', 1234)

    def post(self):
        try:
            args = parser.parse_args()
            user_id = args.get('user_id')
            role_id = args.get('role_id')
            # if user_id and role_id:
            if not all([user_id, role_id]):
                raise Exception('参数错误,参数不能为空')

            role_user_manage.role_user_add(user_id, role_id)
        except Exception as e:
            return set_return_val(False, {}, str(e), 1234), 400
        return set_return_val(True, {}, '用户角色添加成功', 1234)

    def put(self):
        # 更新用户角色
        try:
            args = parser.parse_args()
            user_id = args.get('user_id')
            new_role_id = args.get('new_role_id')
            old_role_id = args.get('old_role_id')

            if not all([user_id, new_role_id, old_role_id]):
                raise Exception('参数错误,参数不能为空')

            role_user_manage.role_user_update(user_id, new_role_id, old_role_id)
        except Exception as e:
            return set_return_val(False, {}, str(e), 1234), 400
        return set_return_val(True, {}, '用户角色更新成功', 1234)

    def delete(self):
        # 删除用户所有角色
        try:
            args = parser.parse_args()
            user_id = args.get('user_id')
            if not user_id:
                raise Exception('参数错误,参数不能为空')
            role_user_manage.role_user_delete(user_id)
        except Exception as e:
            return set_return_val(False, {}, str(e), 1234), 400
        return set_return_val(True, {}, '用户角色删除成功', 1234)
