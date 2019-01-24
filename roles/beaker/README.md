## How to run tox

We use tox to run Molecule, this allow us to easily try different versions of Ansible.

### SELinux

The tox configuration has been tested on Fedora 29, with the
libselinux-python, and SELinux enabled.

You will need the following flag to be able to start MariaDB:

```
# setsebool -P container_manage_cgroup 1
```

### Docker

You also need to install Docker, and ensure your user can access the
daemon directly.

```
$ sudo groupadd docker && sudo gpasswd -a ${USER} docker && sudo systemctl restart docker
$ newgrp docker
```

See: https://developer.fedoraproject.org/tools/docker/docker-installation.html
