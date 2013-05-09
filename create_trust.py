from fabric.api import *

def ssh_keygen():
    run('ssh-keygen')

def get_key():
    local('rm -f ./id_ras.pub')
    get('~/.ssh/id_rsa.pub', './id_rsa.pub')

def put_key():
    put('./id_rsa.pub', '/tmp/')
    run('cat /tmp/id_rsa.pub >> ~/.ssh/authorized_keys2')

def create_relation(from_host, remote_hosts):
    execute(get_key, hosts=[from_host])
    execute(put_key, hosts=remote_hosts)
    local('rm -f ./id_ras.pub')

def auto_ssh(*args):
    """Create ssh trust connection beween host1, host2, ..., hostn
    fab -f create_trust.py auto_ssh:host1,host2,host3,hostN
    """
    if len(args) < 2:
        abort('argument >= 2')

    for (i, from_host) in enumerate(args):
        remote_hosts = list(args[0:i])
        remote_hosts.extend(args[i+1:])
        create_relation(from_host, remote_hosts)

