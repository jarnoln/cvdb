# Fabric deploy file
#
# Usage:
# Localhost:
# fab deploy:host=username@localhost
# Live:
# fab deploy:host=ubuntu@makecv.net

import os
from fabric.contrib.files import exists
from fabric.api import env, local, run, sudo
from fabric.network import ssh


REPO_URL = "git@github.com:jarnoln/cvdb.git"
LOCAL_SITE_NAME = 'local.makecv.net'
ssh.util.log_to_file('fabric_ssh.log')

aws_key_file_path = os.environ.get("AWS_KEY_FILE_PATH", '')
if aws_key_file_path:
    env.key_filename = aws_key_file_path
else:
    print("No AWS key file defined. Not a problem if not deploying to AWS.")


def get_site_name():
    if env.host == 'localhost' or env.host == '127.0.0.1':
        return LOCAL_SITE_NAME
    else:
        return env.host


def deploy():
    site_name = get_site_name()
    site_folder = '/home/%s/sites/%s' % (env.user, site_name)
    source_folder = site_folder + '/source'
    virtualenv = site_folder + '/virtualenv'
    python = virtualenv + '/bin/python'
    pip = virtualenv + '/bin/pip'
    app_list = ['viewcv']
    _create_directory_structure_if_necessary(site_folder)
    _init_virtualenv(site_folder)
    _get_latest_source(source_folder)
    _install_virtualenv_libraries(source_folder, pip)
    _check_secret_key(source_folder, python)
    _update_database(source_folder, python)
    _run_remote_unit_tests(app_list, source_folder, python)
    _restart_nginx(site_name)


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


def _check_secret_key(source_folder, python):
    settings_folder = source_folder + '/cvdb'
    if not exists(settings_folder + '/passwords.py'):
        run('%s %s/generate_passwords.py %s/passwords.py' % (python, settings_folder, settings_folder))


def _update_database(source_folder, python):
    run('cd %s && %s manage.py makemigrations' % (source_folder, python))
    run('cd %s && %s manage.py migrate' % (source_folder, python))


def _run_remote_unit_tests(app_list, source_folder, python):
    print('*** Run remote unit tests')
    for app in app_list:
        run('cd %s && %s manage.py test %s --settings=cvdb.settings' % (source_folder, python, app))


def _restart_nginx(site_name):
    sudo('systemctl restart gunicorn-cvdb')
    sudo('service nginx restart')
