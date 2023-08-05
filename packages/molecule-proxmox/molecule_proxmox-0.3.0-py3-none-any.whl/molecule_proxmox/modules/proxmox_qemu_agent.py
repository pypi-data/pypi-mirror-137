#!/usr/bin/python

# Copyright (c) 2022, Sine Nomine Associates
# BSD 2-Clause License

ANSIBLE_METADATA = {
    'metadata_version': '1.1.',
    'status': ['preview'],
    'supported_by': 'community',
}

DOCUMENTATION = r"""
---
module: proxmox_qemu_agent

short_description: Query the qemu guest agent to find the IP addresses of a running vm.

author:
  - Michael Meffie (@meffie)
"""

EXAMPLES = r"""
"""

RETURN = r"""
"""

import time
import syslog
import pprint

from proxmoxer import ProxmoxAPI
from ansible.module_utils.basic import AnsibleModule


def get_vm(module, proxmox, vmid):
    """
    Look up a vm by id, and fail if not found.
    """
    vm_list = [vm for vm in proxmox.cluster.resources.get(type='vm') if vm['vmid'] == int(vmid)]
    if len(vm_list) == 0:
        module.fail_json(vmid=vmid, msg='VM with vmid = %s not found' % vmid)
    if len(vm_list) > 1:
        module.fail_json(vmid=vmid, msg='Multiple VMs with vmid = %s found' % vmid)
    return vm_list[0]


def get_addresses(interfaces):
    """
    Extract the non-loopback IPv4 addresses from network-get-interfaces results.

    Example:
        interfaces = [
            {'hardware-address': '6e:25:bb:c7:4b:76',
             'name': 'ens18',
             'ip-addresses': [
                {'ip-address': '192.168.136.176', 'ip-address-type': 'ipv4', 'prefix': 24},
                {'ip-address': 'fe80::6c25:bbff:fec7:4b76', 'ip-address-type': 'ipv6', 'prefix': 64},
             ]
             ...
            },
            {'hardware-address': '00:00:00:00:00:00',
             'name': 'lo',
            ...
        ]}]

        get_addresses(interface)
        ['192.168.136.85']

    """
    addrs = []
    for interface in interfaces:
        if 'ip-addresses' in interface:
            for ip_address in interface['ip-addresses']:
                atype = ip_address.get('ip-address-type', '')
                aip = ip_address.get('ip-address', '')
                if aip and atype == 'ipv4' and not aip.startswith('127.'):
                    addrs.append(aip)
    return addrs


def run_module():
    """
    Lookup the IP addresses on a running vm with the qemu guest agent.
    Since the guest may still be booting and acquiring an address with
    DHCP, retry until we find at least one address, or timeout.
    """
    result = dict(
        changed=False,
    )
    module = AnsibleModule(
        argument_spec=dict(
            api_host=dict(type='str', required=True),
            api_user=dict(type='str', required=True),
            api_password=dict(type='str', no_log=True),
            api_token_id=dict(type='str', no_log=True),
            api_token_secret=dict(type='str', no_log=True),
            validate_certs=dict(type='bool', default=False),
            vmid=dict(type='int', required=True),
        ),
        required_together=[('api_token_id', 'api_token_secret')],
        required_one_of=[('api_password', 'api_token_id')],
    )
    api_host = module.params['api_host']
    validate_certs = module.params['validate_certs']
    api_user = module.params['api_user']
    api_password = module.params['api_password']
    api_token_id = module.params['api_token_id']
    api_token_secret = module.params['api_token_secret']
    vmid = module.params['vmid']

    auth_args = {'user': api_user}
    if not (api_token_id and api_token_secret):
        auth_args['password'] = api_password
    else:
        auth_args['token_name'] = api_token_id
        auth_args['token_value'] = api_token_secret

    proxmox = ProxmoxAPI(api_host, verify_ssl=validate_certs, **auth_args)

    retries = 20
    while retries > 0:
        try:
            vm = get_vm(module, proxmox, vmid)
            result['vm'] = vm
            reply = proxmox.nodes(vm['node']).qemu(vmid).agent.get('network-get-interfaces')
            syslog.syslog("reply: %s" % pprint.pformat(reply, compact=True))
            if 'result' in reply:
                interfaces = reply['result']
                addresses = get_addresses(interfaces)
                if addresses:
                    result['vm']['addresses'] = addresses
                    break
        except Exception as e:
            syslog.syslog("Exception type %s" % type(e))
            syslog.syslog(str(e))
            pass
        retries -= 1
        time.sleep(5)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
