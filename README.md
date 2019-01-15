# Beaker installation

This is a playbook to install an all-in-one beaker server & lab controller.
It has been designed to be used with [Distributed-CI](https://doc.distributed-ci.io/) but it can also be used independently of it.

## Download

You can download the role from Github with the following command:

    git clone https://github.com/redhat-cip/ansible-playbook-dci-beaker/
    cd ansible-playbook-dci-beaker

## Initial configuration

Before applying the role, the following files need some configuration:

- `inventory`: adjust the hostname and user of the machine to use as a beaker server
- `group_vars/all`: adjust the values for admin user and lab setup (DHCP range, systems access)

## Deployment

Call Ansible with the following command:

    ansible-playbook -i inventory playbook.yml

---
:warning: For Ansible ≤ 2.5.6 users, you will face a problem with the `service_facts` module. The solution is to skip the firewall tag:

    ansible-playbook -i inventory playbook.yml --skip-tags=firewall
---

## Post-Deployment

After running the playbook the first time, the credentials for services on the beaker server will be stored in the `credentials/` folder, unless the variables ared hardcoded in `group_vars/all`
