#!/bin/bash
set -eux

DATA_STORE=/var/lib/libvirt/images
RHEL_IMG=${DATA_STORE}/rhel-server-7.6-x86_64-kvm.qcow2
INSTANCE_IMG=${DATA_STORE}/beaker-test-cache.qcow2
CACHE_IMG=${INSTANCE_IMG}.cache

sudo dnf install -y libvirt virt-install libguestfs-tools

function kill_instance() {
    sudo virsh destroy beaker-test || true
    sudo virsh undefine beaker-test --remove-all-storage || true
}

function build_cache() {
    sudo cp -v ${RHEL_IMG} ${CACHE_IMG}.temp
    sudo virt-customize -v -x -a  ${CACHE_IMG}.temp \
       --network \
       --sm-register \
       --sm-credentials ${RHSM_LOGIN}:password:${RHSM_PASSWORD} \
       --sm-attach auto \
       --update \
       --ssh-inject "root:file:$HOME/.ssh/id_rsa.pub" \
       --uninstall cloud-init \
       --root-password "file:password.txt" \
       --timezone America/Toronto \
       --sm-unregister \
       --selinux-relabel

    sudo cp -v ${CACHE_IMG}.temp ${CACHE_IMG}
}

function deploy() {
    test -f password.txt || uuidgen > password.txt
    sudo cp -v ${CACHE_IMG} ${INSTANCE_IMG}
    sudo virt-install \
        --import \
        -n beaker-test -r 2048 --vcpus 1 \
        --os-type linux \
        --os-variant rhel7 -v \
        --debug \
        --network network=default \
        --graphics spice \
        --noautoconsole \
        --disk path=${INSTANCE_IMG},size=10,bus=virtio,format=qcow

    sleep 30
    beaker_ip=$(instance_ip)
    echo "beaker ansible_host=$beaker_ip ansible_user=root ansible_ssh_common_args='-o StrictHostKeyChecking=no'" > inventory.test
}

function instance_ip() {
    local mac=$(sudo virsh domiflist beaker-test|awk '/default/ {print $5}')
    sudo virsh net-dhcp-leases default --mac $mac|awk '/ipv4/ {print $5}'|head -n1|sed 's,/.*,,'
}

if [ ! -f ${CACHE_IMG} ]; then
    build_cache
fi

kill_instance
deploy

ansible-playbook -i inventory.test playbook.yml
