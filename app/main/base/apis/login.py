# -*- coding:utf-8 -*-

from flask_restful import Resource, reqparse
from app.models import User
from flask_security import login_user
from flask import session, request

# import redis


parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('id')

ret_data = {
    'ok': True,
    'data': {}
}


class LoginManage(Resource):

    def post(self):
        """
        登录
        ---
        tags:
          - login
        parameters:
          - in: formData
            name: username
            type: string
            required: true
          - in: formData
            name: password
            type: string
            required: true
        responses:
          200:
            description: 用户登录
            schema:
              id: User
              properties:
                id:
                  type: string
                  description: 用户id
                  default: Steven Wilson
                  name: code
        """
        args = parser.parse_args()

        users = User.query.filter_by(username=args['username']).first()
        # print('status:', users.verify_password(args['password']))
        # if not users or not users.verify_password(args['password']):
        if not users:
            ret_data['ok'] = False
            ret_data['msg'] = '账号或密码错误'
            ret_data['code'] = '1001'

        else:
            if not users.verify_password(args['password']):
                ret_data['ok'] = False
                ret_data['msg'] = '账号或密码错误'
                ret_data['code'] = '1001'
            else:
                login_user(users, True)
                token = users.generate_auth_token()
                # token = create_token(users.id, users.username)
                data = {
                    'token': token,
                    'id': users.id,
                    'username': users.username,
                    'email': users.email,
                    'mobile': users.mobile,
                    'department': users.department,
                    'job': users.job,
                    'location': users.location,
                    'sex': users.sex,
                    'remarks': users.remarks
                }
                session[token] = True
                ret_data['data'] = data
                ret_data['code'] = '1000'
        return ret_data

    def get(self):
        print('debug:', request.args.get('debug'))
        print('get')
        return 'ccc'
