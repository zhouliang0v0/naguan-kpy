# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse
from app.exts import db
from app.models import User

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('email')
parser.add_argument('first_name')
parser.add_argument('uid')
parser.add_argument('mobile')
parser.add_argument('department')
parser.add_argument('job')
parser.add_argument('location')
parser.add_argument('company')
parser.add_argument('sex')
parser.add_argument('uac')
parser.add_argument('active')
parser.add_argument('is_superuser')
parser.add_argument('remarks')
parser.add_argument('last_login_ip')
parser.add_argument('current_login_ip')

ret_status = {
    'ok': True,
    'code': 200,
    'msg': '创建成功',
    'data': ''
}

class UserManage(Resource):

    def get(self):
        """
        获取用户信息
        ---
        tags:
          - user
        summary: Add a new pet to the store
        parameters:
          - in: query
            name: id
            type: string
            description: 用户id
          - name: email
            type: string
            in: query
            description: 邮箱
          - name: mobile
            type: string
            in: query
            description: 手机号码
          - name: remarks
            type: string
            in: query
            description: 备注
        responses:
          200:
            description: A single user item
            schema:
              id: User
              properties:
                username:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
        """
        # session = Session()
        args = parser.parse_args()
        try:
            query = db.session.query(User)
            if args['id']:
                query = query.filter_by(id=args['id'])
            if args['email']:
                query = query.filter_by(email=args['email'])
            if args['mobile']:
                query = query.filter_by(mobile=args['mobile'])
            if args['remarks']:
                query = query.filter_by(remarks=args['remarks'])
            data = query.all()
            db.session.remove()
            userinfo = []
            for user in data:
                user = {
                    'name': user.username,
                    'email': user.email
                }
                userinfo.append(user)
            ret_status['data'] = userinfo
            ret_status['msg'] = '成功获取用户信息'
            ret_status['code'] = '1100'
        except Exception, e:
            # pass
            ret_status['code'] = 1102
            # 'msg': '创建成功',
            ret_status['msg'] = '请求异常，请传入正确的参数'
            ret_status['code'] = False
            # print('Exception')
            # userinfo = []

        return ret_status
        # return 'user'

    def post(self):
        """
       新增用户信息
       ---
       tags:
          - user
       parameters:
         - in: formData
           name: username
           type: string
           required: true
         - in: formData
           name: password
           type: string
           required: true
         - in: formData
           name: email
           type: string
           required: true
         - in: formData
           name: first_name
           type: string
           required: true
         - in: formData
           name: uid
           type: string
           required: true
         - in: formData
           name: mobile
           type: string
           required: true
         - in: formData
           name: department
           type: string
           required: true
         - in: formData
           name: job
           type: string
           required: true
         - in: formData
           name: location
           type: string
           required: true
         - in: formData
           name: company
           type: string
           required: true
         - in: formData
           name: sex
           type: string
           required: true
         - in: formData
           name: uac
           type: string
           required: true
         - in: formData
           name: active
           type: string
           required: true
         - in: formData
           name: is_superuser
           type: string
           required: true
         - in: formData
           name: remarks
           type: string
         - in: formData
           name: last_login_ip
           type: string
           required: true
         - in: formData
           name: current_login_ip
           type: string
           required: true
       responses:
         200:
           description: A single user create item
           schema:
             id: User
             properties:
               username:
                 type: string
                 description: The name of the user
                 default: Steven Wilson
        """
        args = parser.parse_args()
        user = User.query.filter(User.username == args['username'])
        email = User.query.filter(User.email == args['email'])
        if user.count() == 0:
            if email.count() == 0:
                newuser = User()
                newuser.username = args['username']
                # newuser.password = args['password']
                newuser.hash_password(args['password'])
                newuser.email = args['email']
                newuser.first_name = args['first_name']
                newuser.uid = args['uid']
                newuser.mobile = args['mobile']
                newuser.department = args['department']
                newuser.job = args['job']
                newuser.location = args['location']
                newuser.company = args['company']
                newuser.sex = args['sex']
                newuser.uac = args['uac']
                # newuser.active = args['active']
                newuser.active = True
                # newuser.is_superuser = args['is_superuser']
                newuser.is_superuser = True
                newuser.remarks = args['remarks']
                newuser.last_login_ip = args['last_login_ip']
                newuser.current_login_ip = args['current_login_ip']
                newuser.login_count = 0

                db.session.add(newuser)
                db.session.commit()

                ret_status['code'] = 1100
                ret_status['msg'] = '用户创建成功'
                ret_status['ok'] = True
            else:
                ret_status['code'] = 1103
                ret_status['msg'] = '邮箱地址已存在'
                ret_status['ok'] = False
                ret_status['data'] = ''
                return ret_status
        else:
            ret_status['code'] = 1103
            ret_status['msg'] = '用户已存在'
            ret_status['ok'] =  False
            ret_status['data'] = ''
            # print('username already exist')
        return ret_status

    # @swag_from('index.yml')
    def put(self, id):
        """
        更新用户信息
        ---
        tags:
          - user
        parameters:
         - in: path
           type: integer
           format: int64
           required: true
         - in: formData
           name: active
           type: string
         - name: password
           type: string
           in: formData
        responses:
         200:
           description: 更新用户名和状态
           schema:
             id: User
             properties:
               username:
                 type: string
                 description: The name of the user
                 default: Steven Wilson
        """

        args = parser.parse_args()
        try:
            user = User.query.filter(User.id == id)
        except Exception, e:
            print('can not find:', id)
            ret_status['code'] = 3000
            ret_status['msg'] = '获取用户信息异常'
            return ret_status

        if user.count() == 1:
            try:
                # User.query.filter(User.id == u_id).update({'active': False})
                if args['password']:
                    User.query.filter(User.id == id).update({'password': args['password']})
                if args['active']:
                    active = args['active']

                    if active.upper() == 'TRUE':
                        active = True
                    elif active.upper() == 'FALSE':
                        active = False
                    else:
                        ret_status['code'] = 3004
                        ret_status['status'] = 'failed'
                        ret_status['msg'] = '参数错误，请传入正确的active状态，true or false'
                        pass
                    User.query.filter(User.id == id).update({'active': active})
                db.session.commit()
                ret_status['msg'] = '更新用户信息成功'
                ret_status['status'] = 'success'
            except Exception, e:
                ret_status['code'] = 3001
                ret_status['msg'] = '更新用户信息异常'
        else:
            ret_status['code'] = 3002
            ret_status['msg'] = '未找到用户'
            ret_status['status'] = 'failed'
        return ret_status

    def delete(self, id):
        """
        根据id用户信息
       ---
       tags:
          - user
       parameters:
         - in: path
           name: id
           type: integer
           format: int64
           required: true
       responses:
         200:
           description: A single user item
           schema:
             id: User
             properties:
               id:
                 type: string
                 description: 用户id
                 default: Steven Wilson
        """
        # args = parser.parse_args()
        try:
            user = User.query.filter(User.id == id).delete()
            db.session.commit()
            ret_status['msg'] = '删除成功'
        except Exception, e:
            ret_status['code'] = 3005
            ret_status['msg'] = '删除失败'
            ret_status['status'] = 'failed'
        return ret_status
