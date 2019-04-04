# -*- coding:utf-8 -*-
from flask_restful import reqparse, Resource, fields, marshal_with
from app.exts import db
from app.models import SystemConfig
from app.main.base.auth import basic_auth
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 系统配置 请求格式
parser = reqparse.RequestParser()
parser.add_argument('platform_name', type=str, required=True, help='请输入平台名称')
parser.add_argument('version_information', type=str, required=True, help='请输入版本信息')
parser.add_argument('copyright', type=str, required=True, help='请输入版权')
parser.add_argument('user_authentication_mode', type=str, required=True, help='用户验证模式')
parser.add_argument('debug', type=bool, required=True, help='是否开启调试模式')


# 自定义格式，fields.Raw
class LogoForm(fields.Raw):
    def format(self, value):
        return '/static/img/' + value


# 日志存储位置
class StoreForm(fields.Raw):
    def format(self, value):
        return '/static/store_log/' + value


# 获取系统配置参数
system_fields = {
    'platform_name': fields.String,
    'version_information': fields.String,
    'logo': LogoForm(attribute='logo'),  # attribute='模型字段名'
    'copyright': fields.String,
    'user_authentication_mode': fields.String,
    'DEBUG': fields.Boolean,
    'STORE_LOG': StoreForm(attribute='store_log'),
}

# 响应 格式
result_fields = {
    'code': fields.Integer,
    'msg': fields.String,
    'ok': fields.Boolean,
    'data': fields.Nested(system_fields)
}

# 更新系统配置资源定制格式
sysconfig_fields = {
    'id': fields.Integer,
    'platform_name': fields.String,  # 平台名称
    'version_information': fields.String,  # 版本号
    'copyright': fields.String,  # 版权
    'user_authentication_mode': fields.String,  # 用户验证模式
    'DEBUG': fields.Boolean,
    'STORE_LOG': fields.String,  # 日志存储位置
}

# 最终显示格式2
result_fields2 = {
    'code': fields.Integer,
    'msg': fields.String,
    'ok': fields.Boolean,
    'data': fields.List(fields.Nested(sysconfig_fields))
}


class System(Resource):
    @basic_auth.login_required
    @marshal_with(result_fields)
    def post(self):
        """
            初始化系统配置
            ---
            tags:
              - system config
            parameters:
              - name: platform_name
                in: query
                type: string
                description: 平台名称
                required: true
              - name: version_information
                type: string
                in: query
                description: 版本信息
              - name: copyright
                type: string
                in: query
                description: 版权
              - name: user_authentication_mode
                type: string
                in: query
                description: 用户验证模式
              - name: debug
                type: boolean
                in: query
                description: debug
            responses:
              200:
                description: A single user item
                schema:
                  description: The system configuration was initialized successfully
                  default: success
        """
        args = parser.parse_args()
        system = SystemConfig()  # 获取配置信息
        system.platform_name = args.get('platform_name').decode("utf-8")
        system.version_information = args.get('version_information').decode("utf-8")
        system.copyright = args.get('copyright').decode("utf-8")
        system.user_authentication_mode = args.get('user_authentication_mode').decode("utf-8")
        system.DEBUG = args.get('debug')

        # 若存在配置，则不允许再创建配置
        systems = SystemConfig.query.all()
        if systems:
            response_data = {
                'code': 404,
                'msg': '系统配置已初始化，配置失败',
                'ok': False,
                'data': ''
            }
            return response_data
        else:
            db.session.add(system)
            db.session.commit()
            # 返回数据
            response_data = {
                'msg': '创建配置成功',
                'ok': True,
                'data': system,
                'code': 201,
            }
            return response_data

    def get(self):
        """
        获取系统配置信息
        ---
        tags:
         - system config
        responses:
          200:
            description: A single user item
            schema:
              id: SystemConfiguration
              properties:
                platform_name:
                  type: string
                version_information:
                  type: string
                logo:
                  type: string
                copyright:
                  type: string
                user_authentication_mode:
                  type: string
                debug:
                  type: boolean
                store_log:
                  type: string
            """
        # parse = parser.parse_args()
        sysconfig = SystemConfig.query.get(1)  # 默认显示所有
        if sysconfig is None:  # 未配置
            response_data = {
                'ok': False,
                'msg': '系统未配置,请求失败',
                'data': '',
                'code': 404,
            }
            return response_data
        else:
            all_config = {
                'platform_name': sysconfig.platform_name,
                'version_information': sysconfig.version_information,
                'logo': sysconfig.logo,
                'copyright': sysconfig.copyright,
                'user_authentication_mode': sysconfig.user_authentication_mode,
                'debug': sysconfig.debug,
                'store_log': sysconfig.store_log
            }
            response_data = {
                'ok': True,
                'msg': '成功请求系统配置信息',
                'data': all_config,
                'code': 200,
            }
            return response_data

    @marshal_with(result_fields2)
    def put(self):
        """
            更新系统配置
            ---
            tags:
              - system config
            parameters:
              - in: query
                name: platform_name
                type: string
                description: 平台名称
              - name: version_information
                type: string
                in: query
                description: 版本信息
              - name: copyright
                type: string
                in: query
                description: 版权
              - name: user_authentication_mode
                type: string
                in: query
                description: 用户验证模式
              - name: debug
                type: boolean
                in: query
                description: debug
            responses:
              200:
                description: A single user item
                schema:
                  description: The system configuration was updated successfully
                  default: success
        """
        args = parser.parse_args()
        system = SystemConfig.query.get(1)
        if system:
            platform_name = args.get('platform_name')
            version_information = args.get('version_information')
            copyright = args.get('copyright')
            user_authentication_mode = args.get('user_authentication_mode')
            debug = args.get('debug')
            if platform_name:
                system.platform_name = platform_name.decode("utf-8")
            if version_information:
                system.version_information = version_information.decode("utf-8")
            if copyright:
                system.copyright = copyright.decode("utf-8")
            if user_authentication_mode:
                system.user_authentication_mode = user_authentication_mode.decode("utf-8")
            if debug:
                system.DEBUG = debug
            db.session.add(system)
            db.session.commit()
            response_data = {
                'msg': '更新系统配置成功',
                'ok': True,
                'data': system,
                'code': 200,
            }
            return response_data
        else:
            response_data = {
                'msg': '未初始化系统配置，修改失败',
                'ok': False,
                'data': '',
                'code': 404,
            }
        return response_data