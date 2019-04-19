# -*- coding:utf-8 -*-
from app.main.vcenter.db import vcenter as db_vcenter
from pyVim import connect
import atexit

# from pyVmomi import vmodl
from pyVmomi import vim


def connect_server(host, user, password, port, ssl=True):
    if ssl:
        service_instance = connect.SmartConnectNoSSL(host=host,
                                                     user=user,
                                                     pwd=password,
                                                     port=int(port))
    else:
        service_instance = connect.SmartConnect(host=host,
                                                user=user,
                                                pwd=password,
                                                port=int(port))
    return service_instance


def sync_vcenter(content, platform):
    options = dict()

    # options = {'type': 1,
    #            'platform_id': platform['id'],
    #            'dc_host_folder_mor_name': None,
    #            'dc_mor_name': None,
    #            'dc_oc_name': None,
    #            'dc_vm_folder_mor_name': None,
    #            'mor_name': None,
    #            'name': None,
    #            'cluster_mor_name': None,
    #            'cluster_oc_name': None
    #            }

    # if platform:

    options['type'] = 1
    options['platform_id'] = platform['id']
    options['dc_host_folder_mor_name'] = None
    options['dc_mor_name'] = None
    options['dc_oc_name'] = None
    options['dc_vm_folder_mor_name'] = None
    options['mor_name'] = None
    options['name'] = platform['platform_name']
    options['cluster_mor_name'] = None
    options['cluster_oc_name'] = None

    db_vcenter.vcenter_tree_create(options)
    datacenters = content.rootFolder.childEntity
    for dc in datacenters:
        # print(dir(dc))
        # print('dc --str--', dc)

        dc_info = '%s' % dc

        dc_mor = dc_info.replace("'", "").split(':', 1)[1]
        # 添加dc 信息

        dchost_info = '%s' % dc.hostFolder
        dchost_moc = dchost_info.replace("'", "").split(':', 1)[1]

        dcvm_info = '%s' % dc.vmFolder
        dcvm_moc = dcvm_info.replace("'", "").split(':', 1)[1]
        options['type'] = 2
        options['dc_mor_name'] = dc_mor
        options['dc_oc_name'] = dc.name
        options['mor_name'] = dc_mor
        options['name'] = dc.name
        options['dc_host_folder_mor_name'] = dchost_moc
        options['dc_vm_folder_mor_name'] = dcvm_moc

        db_vcenter.vcenter_tree_create(options)
        print('datacenter_mor:' + dc_mor)
        print('datacenter:' + dc.name)
        # if hasattr(dc, 'vmFolder'):
        #     vmFolders = dc.vmFolder
        #     print(vmFolders)

        print('hostfolder_mor:', dc.hostFolder)
        print('vmfolder_mor:', dc.vmFolder)
        # print('hostfolder:', dc.hostFolder.name)
        clusters = dc.hostFolder.childEntity
        # print(clusters.name)
        for cluster in clusters:
            # print('cluster.Folder', cluster.vmFolder)
            # print(dir(cluster))
            # print(cluster.summary)
            # print(dir(host))
            print('resourcePool:', cluster.resourcePool)

            resourcePool = '%s' % cluster.resourcePool
            resourcePool_mor = resourcePool.replace("'", "").split(':', 1)[1]
            print('resourcePool:', cluster.resourcePool.name)

            cluster_info = '%s' % cluster
            cluster_mor = cluster_info.replace("'", "").split(':', 1)[1]

            # 添加 cluster 信息
            options['type'] = 3
            options['cluster_mor_name'] = cluster_mor
            options['cluster_oc_name'] = cluster.name
            options['mor_name'] = cluster_mor
            options['name'] = cluster.name
            db_vcenter.vcenter_tree_create(options)
            print('  cluster_mor:', cluster_mor)
            print('  cluster:', cluster.name)

            hosts = cluster.host
            for host in hosts:
                # print(host)


                host_info = '%s' % host
                host_mor = host_info.replace("'", "").split(':', 1)[1]
                print('    host mor:', host_mor)
                print('    host namne:', host.name)

                # 添加host信息
                options['type'] = 4
                options['mor_name'] = host_mor
                options['name'] = host.name
                db_vcenter.vcenter_tree_create(options)

                hostname = host.summary.config.name
                print(hostname)
                vms = host.vm
                # print(vms)
                for vm in vms:
                    # print(vm)
                    vm_info = '%s' % vm
                    vm_mor = vm_info.replace("'", "").split(':', 1)[1]
                    # print('        vm_mor:', vm_mor)
                    # print('        vm:', vm.summary.config.name)
    return 'cccc'
