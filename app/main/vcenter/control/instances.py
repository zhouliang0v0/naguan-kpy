# -*- coding:utf-8 -*-
from pyVim import connect
import atexit

from pyVmomi import vmodl
from pyVmomi import vim
from app.main.base.control import cloud_platform
from app.main.vcenter.control.vcenter import connect_server, sync_vcenter


def PrintVmInfo(vm, depth=1):
    # """
    # Print information for a particular virtual machine or recurse into a folder
    # or vApp with depth protection
    # """
    maxdepth = 10

    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        if depth > maxdepth:
            return
        vmList = vm.childEntity
        for c in vmList:
            PrintVmInfo(c, depth + 1)
        return

    # if this is a vApp, it likely contains child VMs
    # (vApps can nest vApps, but it is hardly a common usecase, so ignore that)
    if isinstance(vm, vim.VirtualApp):
        vmList = vm.vm
        for c in vmList:
            PrintVmInfo(c, depth + 1)
        return

    summary = vm.summary
    # print("Name       : ", summary.config.name)
    # print("Path       : ", summary.config.vmPathName)
    # print("Guest      : ", summary.config.guestFullName)
    annotation = summary.config.annotation
    if annotation != None and annotation != "":
        print("Annotation : ", annotation)
    # print("State      : ", summary.runtime.powerState)
    if summary.guest != None:
        ip = summary.guest.ipAddress
        if ip != None and ip != "":
            # print("IP         : ", ip)
            pass
    if summary.runtime.question != None:
        print("Question  : ", summary.runtime.question.text)
    # print("")


def get_cluster(clusters):
    pass


def vm_list_all(options=None):

    options = {
        'id': 1
    }

    # 获取云平台
    platforms = cloud_platform.platform_list(options)
    # print('platform', platforms)
    if platforms:
        platform = platforms[0]
        s = connect_server(platform['ip'], platform['name'], platform['password'], platform['port'])
        atexit.register(connect.Disconnect, s)
    else:
        raise Exception('unable to find platform')
    content = s.RetrieveContent()

    sync_vcenter(content, platforms[0])

    return 'ccc'
    # print(dir(content.rootFolder))
    # obj_view = content.viewManager.CreateContainerView(content.rootFolder,
    #                                                    [vim.StoragePod],
    #                                                    True)
    # exist_host = obj_view.view


    dcs = content.rootFolder.childEntity
    # print(children)

    data =[]
    for dc in dcs:
        print('datacenter:' + dc.name)

        # 获取集群
        all_cluster = get_cluster(dc.hostFolder.childEntity)

        clusters = dc.hostFolder.childEntity
        # print(clusters.name)
        for cluster in clusters:
            # print('cluster.Folder', cluster.vmFolder)
            # print(dir(cluster))
            print('  cluster:', cluster.name)
            hosts = cluster.host
            for host in hosts:

                print('resourcePool:', host.resourcePool)

                print('    host namne:', host.name)
                hostname = host.summary.config.name
                # print(host.vm)
                vms = host.vm
                # print(vms)
                for vm in vms:
                    print('        vm:', vm.summary.config.name)
            # if hasattr(cluster, 'vmFolder'):
            #     print('has vmFolder')
            # else:
            #     print(cluster.summary)
            #     print('no vmFolder')

            # print('cluster:', cluster.name)
            # print('network:', cluster.network)
            # print(dir(cluster))
            # hosts = cluster.host
            # for host in hosts:
            #     # print(host.name)
            #     print('host:', host.name)
            #     hostname = host.summary.config.name


        print('')

        """
        if hasattr(child, 'vmFolder'):
            vmFolder = child.vmFolder
            print('vmFolder')
            print(vmFolder.childEntity)
            vmlist = vmFolder.childEntity
            for vm in vmlist:
                # print(vm.name)
                # if hasattr(vm, 'VirtualMachine'):
                #     print(vm)
                #     print(vm.name)
                print(vm.name)
                if hasattr(vm, 'childEntity'):
                    print(vm)
                    vms = vm.childEntity
                    for vm in vms:
                        print(vm.parent)
                        print(vm.name)
                    # print(vms)
                else:
                    print('no vmFolder')
            # print(vmFolder.name)
        """
        """
        vmFolder = child.vmFolder.childEntity
        print(vmFolder)

        if hasattr(vmFolder, 'childEntity'):
            vmFolder = vmFolder.childEntity
            print(vmFolder)
        else:
            for vms in vmFolder:
                print(vms)
        """
                # vm = vms.summary
                # print(vm.config.name)
        # for vm in vmFolder:
        #     print('vm:' + vm)

    # print('exist_host:', exist_host)
    # for ds_cluster in exist_host:
    #     # print(dir(ds_cluster))
    #     # print()
    #     # for vals, key in ds_cluster:
    #         # print('key:', key, 'vals:', vals)
    #     print('ds_cluster:', ds_cluster.name )

    # Folder                                [vim.Folder ]
    # Datacenter                                [vim.Datacenter]
    # ComputeResource                                  [vim.ComputeResource]
    # ResourcePool                                  [vim.ResourcePool]
    # HostSystem                                 [vim.HostSystem]
    # Datastore                                             [vim.Datastore]
    #                                                        StoragePod


    # print(dir(vim))
        # if ds_cluster.name == args.dscluster:
        # datastores = ds_cluster.childEntity
        # print "Datastores: "
        # for datastore in datastores:
        #     print datastore.name

    # print(dir(content))
    # for child in content.rootFolder.childEntity:
    #     if hasattr(child, 'vmFolder'):
    #         datacenter = child
    #         vmFolder = datacenter.vmFolder
    #         vmList = vmFolder.childEntity
    #         for vm in vmList:
    #             PrintVmInfo(vm)
    return 'test'
