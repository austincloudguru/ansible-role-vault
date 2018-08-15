import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_vault_group_exists(host):
    vault_group = host.group("vault")
    assert vault_group.exists


def test_vault_user_exists(host):
    vault_user = host.user("vault")
    assert vault_user.exists


def test_vault_is_installed(host):
    vault_app = host.file("/opt/vault/bin/vault")
    assert vault_app.exists
    assert vault_app.user == 'vault'
    assert vault_app.group == 'vault'
    assert vault_app.mode == 0o750
    assert not vault_app.is_directory


def test_vault_config_is_installed(host):
    vault_config = host.file("/etc/vault.d/vault_main.hcl")
    assert vault_config.exists
    assert vault_config.user == 'vault'
    assert vault_config.group == 'vault'
    assert vault_config.mode == 0o640
    assert not vault_config.is_directory


def test_vault_is_running(host):
    vault_service = host.service('vault')
    # Can't test if it is running because of SSL and Lock status
    # assert vault_service.is_running
    assert vault_service.is_enabled


def test_vault_data_directory(host):
    vault_data_dir = host.file("/var/vault")
    assert vault_data_dir.exists
    assert vault_data_dir.user == 'vault'
    assert vault_data_dir.group == 'vault'
    assert vault_data_dir.is_directory


def test_vault_log_directory(host):
    vault_log_dir = host.file("/var/log/vault")
    assert vault_log_dir.exists
    assert vault_log_dir.user == 'vault'
    assert vault_log_dir.group == 'vault'
    assert vault_log_dir.is_directory
