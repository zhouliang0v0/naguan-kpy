# -*- coding:utf-8 -*-
from flask_restful import Resource, reqparse


parser = reqparse.RequestParser()


class VCenterManage(Resource):
    def get(self):
        """
         获取vCenter tree 信息
        ---
        tags:
          - vCenter tree
        parameters:
          - in: query
            name: id
            type: string
            required: true
        responses:
          200:
            description: vCenter tree 信息
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                code:
                  type: "integer"
                  format: "int64"
                msg:
                  type: string
                data:
                  type: array
                  items:
                    properties:
                      id:
                        type: string
                        default: 1
                      type:
                        type: string
                      platform_id:
                        type: string
                      dc_host_folder_mor_name:
                        type: string
                      dc_mor_name:
                        type: string
                      dc_oc_name:
                        type: string
                      cluster_mor_name:
                        type: string
                      cluster_oc_name:
                        type: string
                      mor_name:
                        type: string
                      name:
                        type: string
                      dc_vm_folder_mor_name:
                        type: string
          400:
            description: 获取失败
            schema:
              properties:
                ok:
                  type: boolean
                  description: 状态
                  default: False
                code:
                  type: "integer"
                  format: "int64"
                  default: 1302
                msg:
                  type: string
                  default: "获取失败"
                data:
                  type: array
                  items:
                    properties:
        """
        parser.add_argument('id')

        pass

    def post(self):

        pass

    def delete(self):
        pass

    def put(self):
        pass