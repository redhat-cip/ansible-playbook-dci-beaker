import os
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_iptables_rules(host):
    rules = host.iptables.rules('filter', 'IN_public_allow')

    expected_ports = {'22', '80', '67', '53', '69', '8000'}
    open_ports = set()

    for rule in rules:
        m = re.search(
            '--dport (\d+) -m conntrack --ctstate NEW -j ACCEPT',
            rule)
        if not m:
            continue
        open_ports.add(m.group(1))
    assert open_ports == expected_ports
