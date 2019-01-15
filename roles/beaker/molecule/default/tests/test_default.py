import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_beaker_services_running_and_enabled(host):
    services = ['beaker-provision', 'beaker-proxy',
                'beaker-watchdog', 'beakerd']
    for service_name in services:
        service = host.service(service_name)
        assert service.is_running
        assert service.is_enabled


def test_dnsmasq_running_and_enabled(host):
    service = host.service('dnsmasq')
    assert service.is_running
    assert service.is_enabled


def test_httpd_running_and_enabled(host):
    service = host.service('httpd')
    assert service.is_running
    assert service.is_enabled


def test_beaker_init(host):
    assert host.run('beaker-init --check').rc == 0


def test_labcontrol_is_populated(host):
    ret = host.run('bkr labcontroller-list')
    assert ret.rc == 0
    assert ret.stdout


def test_beaker_tasks_list(host):
    tasks_expected = {
        '/distribution/check-install',
        '/distribution/command',
        '/distribution/install',
        '/distribution/inventory',
        '/distribution/pkginstall',
        '/distribution/rebuild',
        '/distribution/reservesys',
        '/distribution/updateDistro',
        '/distribution/utils/dummy',
        '/distribution/virt/image-install',
        '/distribution/virt/install',
        '/distribution/virt/start',
        '/distribution/virt/start_stop',
        '/distribution/virt/stop',
        '/kernel/distribution/ltp-nfs/ltp',
    }
    bkr_task_list_ret = host.run('bkr task-list')
    tasks_found = set(bkr_task_list_ret.stdout.split('\n'))
    assert tasks_found == tasks_expected
