# -*- coding:utf-8 -*-

from app.main.base.apis.system import System
from app.main.base.apis.system_logo import SystemLogo

from app.main.base.apis.users import UserManage
from app.main.base.apis.auth import AuthManage
from app.main.base.apis.menus import MenuManage
from app.main.base.apis.login import LoginManage
from app.main.base.apis.cloud_platform import CloudPlatformManage
from app.main.base.apis.platform_type import PlatformTypeMg
from app.main.vcenter.apis.instances import InstanceManage
from app.main.vcenter.apis.vcenter import VCenterManage
from app.main.vcenter.apis.images import ImageManage

from app.main.base.apis.event_logs import LogEvent
from app.main.base.apis.request_logs import LogRequest
from app.main.base.apis.task_logs import LogTask

from flask_restful import Api
from flasgger import Swagger

api = Api()


def restful_init(app):
    api.init_app(app)


def swagger_init(app):
    Swagger(app)


# 登录管理
api.add_resource(LoginManage, '/api/v1.0/login/', endpoint='LoginManage')

# 用户管理
api.add_resource(UserManage, '/api/v1.0/user/', methods=['POST', 'GET'], endpoint='UserManage')
api.add_resource(UserManage, '/api/v1.0/user/<id>', methods=['DELETE', 'PUT'], endpoint='UserMgById')
api.add_resource(AuthManage, '/api/v1.0/sso/auth/', endpoint='AuthManage')

# 菜单管理
api.add_resource(MenuManage, '/api/v1.0/menu/', methods=['GET', 'POST'], endpoint='MenuMg')
api.add_resource(MenuManage, '/api/v1.0/menu/<id>', methods=['PUT', 'DELETE'], endpoint='MenuMgById')

# 系统配置
api.add_resource(System, '/api/v1.0/system/config/')
api.add_resource(SystemLogo, '/api/v1.0/system/Logo/')

# 请求日志
api.add_resource(LogRequest, '/api/v1.0/log/request/', methods=['GET'], endpoint='LogRequest')
api.add_resource(LogRequest, '/api/v1.0/log/request/<int:id>', methods=['DELETE'], endpoint='LogRequestById')

# 事件日志
api.add_resource(LogEvent, '/api/v1.0/log/event/',  methods=['GET'], endpoint='LogEvent')
api.add_resource(LogEvent, '/api/v1.0/log/event/<int:id>', methods=['DELETE'], endpoint='LogEventById')

# 任务日志
api.add_resource(LogTask, '/api/v1.0/log/task/', methods=['GET'], endpoint='LogTask')
api.add_resource(LogTask, '/api/v1.0/log/task/<int:id>', methods=['DELETE'], endpoint='LogTaskById')

# 第三方平台管理
api.add_resource(CloudPlatformManage, '/api/v1.0/platform/', methods=['GET', 'POST'], endpoint='PlatformMg')
api.add_resource(CloudPlatformManage, '/api/v1.0/platform/<id>', methods=['PUT', 'DELETE'], endpoint='PlatformMgById')

# 第三方平台类型管理
api.add_resource(PlatformTypeMg, '/api/v1.0/platform_type/', methods=['GET', 'POST'], endpoint='PfTypeMg')
api.add_resource(PlatformTypeMg, '/api/v1.0/platform_type/<id>', methods=['PUT', 'DELETE'], endpoint='PfTypeMgById')

# vCenter 信息同步
api.add_resource(VCenterManage, '/api/v1.0/vCenter/tree/',  methods=['GET', 'POST', 'PUT', 'DELETE'], endpoint='TreeMg')
api.add_resource(InstanceManage, '/api/v1.0/vm/',  methods=['GET', 'POST', 'PUT', 'DELETE'],  endpoint='VmMg')
api.add_resource(ImageManage, '/api/v1.0/image/',  methods=['GET', 'POST', 'PUT', 'DELETE'],  endpoint='ImageMg')

