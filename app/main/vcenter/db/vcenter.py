# -*- coding:utf-8 -*-
from app.models import VCenterTree
from app.exts import db


# 添加vcenter tree 信息
def vcenter_tree_create(options):

    # print(options)
    new_vcenter = VCenterTree()
    new_vcenter.type = options.get('type')
    new_vcenter.platform_id = options.get('platform_id')
    new_vcenter.dc_host_folder_mor_name = options.get('dc_host_folder_mor_name')
    new_vcenter.dc_mor_name = options.get('dc_mor_name')
    new_vcenter.dc_oc_name = options.get('dc_oc_name')
    new_vcenter.dc_vm_folder_mor_name = options.get('dc_vm_folder_mor_name')
    new_vcenter.mor_name = options.get('mor_name')
    new_vcenter.name = options.get('name')
    new_vcenter.cluster_mor_name = options.get('cluster_mor_name')
    new_vcenter.cluster_oc_name = options.get('cluster_oc_name')

    print(new_vcenter)
    db.session.add(new_vcenter)
    db.session.commit()
    # pass

