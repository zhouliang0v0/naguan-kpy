# -*- coding:utf-8 -*-
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask_restful import Resource, reqparse
from app.models import User
from flask_security import login_user
import os
from config import config


parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('id')

current_config = os.getenv('FLASK_CONFIG') or 'default'
config_dict = config[current_config]
serializer = Serializer(config_dict.SECRET_KEY, expires_in=43200)


ret_data = {
    'ok': True,
    'data': {}
}
def create_token(user_id, username):
    """生成token"""
    data = {
        'id': user_id,
        'username': username
    }
    token = serializer.dumps(data)
    return token.decode("utf-8")


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
        print('status:', users.verify_password(args['password']))
        if not users or not users.verify_password(args['password']):

            ret_data['ok'] = False
            ret_data['msg'] = '账号或密码错误'
            ret_data['code'] = '1001'

        else:
            login_user(users, True)
            token = create_token(users.id, users.username)
            data = {
                'token': token
            }
            ret_data['data'] = data
            ret_data['code'] = '1000'
        return ret_data

    def get(self):
        print('get')
