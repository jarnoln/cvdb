# Fabric deploy file
#
# Usage:
# Localhost:
# fab -f fabfile.py deploy:host=username@localhost
# Live:
# fab -f fabfile.py deploy:host=ec2user@makecv.net

from fabric.contrib.files import exists
from fabric.api import env, local, run, sudo
from fabric.network import ssh


REPO_URL = "git@github.com:jarnoln/cvdb.git"
ssh.util.log_to_file('fabric_ssh.log')


def get_site_name():
    return 'makecv.net'


def deploy():
    site_name = get_site_name()
    site_folder = '/home/%s/sites/%s' % (env.user, site_name)
    source_folder = site_folder + '/source'
    virtualenv = site_folder + '/virtualenv'
    python = virtualenv + '/bin/python'
    pip = virtualenv + '/bin/pip'

    _create_directory_structure_if_necessary(site_folder)
    _init_virtualenv(site_folder)
    _get_latest_source(source_folder)
    _install_virtualenv_libraries(source_folder, pip)


def _create_directory_structure_if_necessary(site_folder):
    run('mkdir -p %s' % site_folder)
    for sub_folder in ('database', 'log', 'static'):
        run('mkdir -p %s/%s' % (site_folder, sub_folder))


def _init_virtualenv(site_folder):
    if not exists(site_folder + '/virtualenv'):
        run('cd %s && virtualenv virtualenv' % site_folder)
    if not exists(site_folder + '/db'):
        run('cd %s && mkdir db' % site_folder)


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % source_folder)
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))

    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _install_virtualenv_libraries(source_folder, pip):
    run('cd %s && %s install -r requirements.txt' % (source_folder, pip))
