import os
import pytest
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("port", [
    ('22'), ('80'), ('67'), ('53'), ('69'),
    ('8000'), ('11')])
def test_iptables_rules(host, port):
    with host.sudo():
        rules = host.iptables.rules('filter', 'IN_public_allow')

    open_ports = set()

    for rule in rules:
        m = re.search(
            '--dport (\d+) -m conntrack --ctstate NEW -j ACCEPT',
            rule)
        if m:
            open_ports.add(m.group(1))
    assert port in open_ports, 'Port %s is not opened' % port
