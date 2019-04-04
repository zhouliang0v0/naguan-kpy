# -*- coding:utf-8 -*-
import uuid

from flask_restful import Resource, reqparse

from app.exts import db
from app.models import Menu
from app.main.base.auth import basic_auth

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('ico')
parser.add_argument('url')
parser.add_argument('name')
parser.add_argument('identifier')
parser.add_argument('id_hide')
parser.add_argument('is_hide_children')
parser.add_argument('important')
parser.add_argument('parent_id')


ret_status = {
    'ok': True,
    'code': 200,
    'msg': '创建成功',
    'data': ''
}

class MenuManage(Resource):

    @basic_auth.login_required
    def get(self):
        """
        获取菜单信息
        ---
        tags:
          - menu
        parameters:
          - in: query
            name: id
            type: string
          - in: query
            name: url
            type: string
          - in: query
            name: name
            type: string
          - in: query
            name: identifier
            type: string
        responses:
          200:
            description: 菜单获取
            schema:
              id: User
              properties:
                id:
                  type: string
                  description: 用户id
                  default: Steven Wilson
                  name: code
        """
        try:

            args = parser.parse_args()
            # print(args['id'])
            query = db.session.query(Menu)
            if args['id']:
                query = query.filter_by(id=args['id'])
            if args['url']:
                query = query.filter_by(url=args['url'])
            if args['name']:
                query = query.filter_by(name=args['name'])
            if args['identifier']:
                query = query.filter_by(identifier=args['identifier'])

            result = query.all()

            # db.session.remove()
            data = []
            for menu in result:
                # print(menu.name)
                menu_tmp = {
                    'id': menu.id,
                    'name': menu.name,
                    'ico': menu.ico,
                    'url': menu.url,
                    'identifier': menu.identifier,
                }
                data.append(menu_tmp)
            ret_status['data'] = data
            ret_status['msg'] = '获取菜单成功'
            ret_status['code'] = 1310
            ret_status['ok'] = True
        except Exception, e:
            ret_status['data'] = ''
            ret_status['msg'] = '获取菜单异常'
            ret_status['code'] = 1319
            ret_status['ok'] = False
        return ret_status

    def post(self):
        """
        提交新的菜单
        ---
        tags:
          - menu
        parameters:
          - in: formData
            name: ico
            type: string
          - in: formData
            name: url
            type: string
          - in: formData
            name: name
            type: string
          - in: formData
            name: identifier
            type: string
          - in: formData
            name: id_hide
            type: string
          - in: formData
            name: is_hide_children
            type: string
          - in: formData
            name: important
            type: string
          - in: formData
            name: parent_id
            type: string
        responses:
          200:
            description: 菜单获取
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
        try:

            new_menu = Menu()
            new_menu.ico = args['ico']
            new_menu.url = args['url']
            new_menu.name = args['name']
            new_menu.identifier = args['identifier']
            new_menu.id_hide = False
            new_menu.is_hide_children = False
            new_menu.important = args['important']
            if args['parent_id']:
                parent_menu = db.session.query(Menu).filter_by(id=args['parent_id']).first()
                if parent_menu:
                    new_menu.parent_id = args['parent_id']
                else:
                    new_menu.parent_id = 0
            else:
                new_menu.parent_id = 0

            db.session.add(new_menu)
            db.session.commit()
            ret_status['data'] = ''
            ret_status['msg'] = '创建菜单成功'
            ret_status['code'] = 1300
            ret_status['ok'] = True
        except Exception, e:
            ret_status['data'] = ''
            ret_status['msg'] = '创建菜单异常，请提交正确的参数'
            ret_status['code'] = 1309
            ret_status['ok'] = False

        return ret_status

    def delete(self, id):
        """
        根据ID删除菜单信息
       ---
       tags:
          - menu
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
        try:
            query = db.session.query(Menu)
            menu = query.filter_by(id=id).first()

            if menu:
                children_menu = query.filter_by(parent_id=id).all()
                if children_menu.count > 0:
                    ret_status['data'] = ''
                    ret_status['msg'] = '当前菜单存在子菜单，请先删除子菜单然后在操作'
                    ret_status['code'] = 1309
                    ret_status['ok'] = False
                else:

                    query.filter_by(id=id).delete()
                    ret_status['data'] = ''
                    ret_status['msg'] = '删除菜单成功'
                    ret_status['code'] = 1300
                    ret_status['ok'] = True
            db.session.commit()
        except Exception, e:
            ret_status['data'] = ''
            ret_status['msg'] = '无法获取到菜单'
            ret_status['code'] = 1309
            ret_status['ok'] = False
        return ret_status

    def put(self, id):
        """
        更新菜单信息
        ---
        tags:
          - menu
        parameters:
         - in: path
           name: id
           type: integer
           format: int64
           required: true
         - in: formData
           name: ico
           type: string
         - name: name
           type: string
           in: formData
         - name: url
           type: string
           in: formData
         - name: identifier
           type: string
           in: formData
         - name: id_hide
           type: string
           in: formData
         - name: is_hide_children
           type: string
           in: formData
         - name: parent_id
           type: string
           in: formData
         - name: important
           type: string
           in: formData
        responses:
         200:
           description: 更新菜单信息
           schema:
             id: User
             properties:
               username:
                 type: string
                 description: The name of the user
                 default: Steven Wilson
        """
        args = parser.parse_args()
        query = db.session.query(Menu)
        try:
            menu = query.filter_by(id=id).first()
            if menu:
                if args['ico']:
                    menu.ico = args['ico']
                if args['name']:
                    menu.name = args['name']
                if args['url']:
                    menu.url = args['url']
                if args['identifier']:
                    menu.identifier = args['identifier']
                if args['id_hide']:
                    menu.id_hide = args['id_hide']
                if args['is_hide_children']:
                    menu.is_hide_children = args['is_hide_children']
                if args['parent_id']:
                    menu.parent_id = args['parent_id']
                if args['important']:
                    menu.important = args['important']
                db.session.commit()
                ret_status['data'] = ''
                ret_status['msg'] = '更新菜单成功'
                ret_status['code'] = 1320
                ret_status['ok'] = True
            else:
                ret_status['data'] = ''
                ret_status['msg'] = '不存在当前菜单'
                ret_status['code'] = 1328
                ret_status['ok'] = False
        except Exception, e:
            ret_status['data'] = ''
            ret_status['msg'] = '获取当前菜单异常，请重试'
            ret_status['code'] = 1329
            ret_status['ok'] = False

        return ret_status