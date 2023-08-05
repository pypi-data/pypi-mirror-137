***********************
Molecule Proxmox Plugin
***********************

This is an experimental Ansible Molecule Driver plugin to manage instances on a
`Proxmox VE`_ hypervisor cluster.  Only virtual machines are supported at this
time.  Proxmox containers will be supported in a future release.

Requirements
============

* Access to a `Proxmox VE`_ cluster
* One or more virtual machine templates with required setup
* Python package `proxmoxer`_
* Ansible module `community.general.proxmox_kvm`_

The required Python packages are automatically installed when
``molecule-proxmox`` is installed with ``pip``.

The ``proxmox_kvm`` module is included with the Community.General collection
and is automatically installed when Ansible is installed with ``pip``.


Virtual machine template requirements
-------------------------------------

The molecule instances are created by cloning Proxmox virtual machine
templates.  You will need to create one or more templates.

Templates have the following requirements.

* networking configured
* Python installed for Ansible
* qemu-guest-agent installed and enabled in Proxmox
* ssh server installed
* user account for Ansible
* An ssh public key must be added to the ``authorized_keys`` for the Ansible user account.
* If a non-root user is used for the Ansible user (recommended), that user should be
  added to the sudoers. (This is not needed for the driver, but will likely be needed
  for the ``converge`` playbook.)


Example
=======

.. code-block:: yaml

   driver:
     name: proxmox
     options:
        api_host: pve01.example.com
        api_user: molecule
        api_password: "********"
        node: pve01
        ssh_user: tester
        ssh_identity_file: /path/to/id_rsa
   platforms:
     - name: test01
       template_vmid: 9000
     - name: test02
       template_vmid: 9000

.. code-block:: yaml

   driver:
     name: proxmox
     options:
        api_host: pve01.example.com
        api_user: molecule
        api_token_id: "********"
        api_token_secret: "*******************************"
        node: pve01
        ssh_user: tester
        ssh_identity_file: /path/to/id_rsa
   platforms:
     - name: test01
       template_vmid: 9000
     - name: test02
       template_vmid: 9000

.. code-block:: yaml

   driver:
     name: proxmox
     options:
        # Secrets file may be encrypted with ansible-vault.
        proxmox_secrets: /path/to/proxmox_secrets.yml"
        node: pve01
        ssh_user: tester
        ssh_identity_file: /path/to/id_rsa
   platforms:
     - name: test01
       template_vmid: 9000
     - name: test02
       template_vmid: 9000

Authors
=======

Molecule Proxmox Plugin was created by Michael Meffie based on code from
Molecule.

License
=======

The `MIT`_ License.


.. _`Proxmox VE`: https://www.proxmox.com/en/proxmox-ve
.. _`proxmoxer`: https://pypi.org/project/proxmoxer/
.. _`community.general.proxmox_kvm`: https://docs.ansible.com/ansible/latest/collections/community/general/proxmox_kvm_module.html
.. _`MIT`: https://github.com/meffie/molecule-proxmox/blob/master/LICENSE
