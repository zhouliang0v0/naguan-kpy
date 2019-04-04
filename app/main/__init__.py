# -*- coding:utf-8 -*-

from app.main.base.system_api import System
from app.main.base.system_logo_api import SystemLogo

from app.main.base.user import UserManage
from app.main.base.auth import AuthManage
from app.main.base.menu import MenuManage
from app.main.base.login import LoginManage

from flask_restful import Api
from flasgger import Swagger

# from flask import Blueprint

# main_v1_bp = Blueprint('main_api', __name__)

api = Api()


def restful_init(app):
    api.init_app(app)


def swagger_init(app):
    Swagger(app)


# 添加资源

api.add_resource(LoginManage, '/ulogin/', endpoint='LoginManage')
api.add_resource(UserManage, '/user/', methods=['POST', 'GET'], endpoint='UserManage')
api.add_resource(UserManage, '/user/<id>', methods=['DELETE', 'PUT'], endpoint='UserManageById')
api.add_resource(AuthManage, '/sso/auth/', endpoint='AuthManage')
api.add_resource(MenuManage, '/menu/', methods=['GET', 'POST'], endpoint='MenuManage')
api.add_resource(MenuManage, '/menu/<id>', methods=['PUT', 'DELETE'], endpoint='MenuManageById')

api.add_resource(System, '/system/config/')
api.add_resource(SystemLogo, '/system/Logo/')
