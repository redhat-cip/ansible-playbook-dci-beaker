# Libvirt based test

## RHEL image and libvirt

First you need to install and start libvirt:

    dnf install -y libvirt
    dnf start libvirt

Then you can copy your RHEL 7.6 cloud image in the default image store:

    cp -v rhel-server-7.6-x86_64-kvm.qcow2 /var/lib/libvirt/images/

## Trigger the test script

    ./run_test.sh

# Molecule

## Install and starts docker

    dnf install docker
    systemctl start docker

## Installation of Molecule

Prepare a virtual environment and Install the dependencies

    virtualenv -p python3 .venv
    source .venv/bin/activate
    pip install molecule ansible docker

## Run Molecule

    source .venv/bin/activate
    cd roles/beaker
    molecule test 
