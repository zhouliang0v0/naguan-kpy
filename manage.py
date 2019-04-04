# -*- coding:utf-8 -*-

from flask_migrate import MigrateCommand
from flask_script import Manager
from app.main.base.auth import basic_auth
from app import create_app
from flask import g
import json
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.before_first_request
def first_request():
    with open('policy.json', 'r') as f:
        json_dict = json.load(f)
    # print(g.policy)
    app.config['POLICY'] = json_dict


@app.before_request
def test():
    g.username = ''



@app.after_request
def after_request(response):

    print('g.user:', g.username)

    return response

# @app.after_request
# def after_request():
#     print(g.username)
#

# def

#
# @app.before_request
# @httpauth.login_required
# def check_policy():
#     # 从config中获取policy
#     print('check_policy')
#     g.policy = app.config['POLICY']
#     if request.path.count('/') == 1:
#         endpoint = request.path.strip('/')
#     else:
#         url_list = request.path.split('/')
#         if url_list[0]:
#             endpoint = ':'.join(url_list)
#         else:
#             del url_list[0]
#             endpoint = ':'.join(url_list)
#
#     # 判断权限
#     if endpoint in g.policy:
#         policy = g.policy[endpoint]
#         if policy:
#             if '_or_' in policy:
#                 need_policy_list = policy.split(':')[1].split('_or_')
#             else:
#                 need_policy_list = [policy.split(':')[1]]
#
#             print(need_policy_list)
#         else:
#             need_policy_list = []
#         # print(dir(current_user))
#         if need_policy_list:
#             for policy_tmp in need_policy_list:
#                 if current_user.has_role(policy_tmp):
#                     policy_flag = True
#                     break
#                 else:
#                     policy_flag = False
#             if not policy_flag:
#                 data = {
#                     'status': 0,
#                     'msg': '用户没有权限访问接口',
#                     'data': ''
#                 }
#                 return jsonify(data)
#
#     else:
#         print(endpoint, 'not in policy')


manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
