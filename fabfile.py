# -*- coding: utf-8 -*-
import datetime
import subprocess
import os

from fabric.api import run, sudo
from fabric.contrib.project import rsync_project
from fabric.contrib.files import sed

DEPLOY_VERSION = os.environ.get('DEPLOY_VERSION', datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))


def deploy():
    p = subprocess.Popen(
        ('git', 'rev-parse', 'HEAD'),
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    revision = p.stdout.read().strip()

    remote_dir = "/var/apps/django-sample-app/releases/{0}".format(DEPLOY_VERSION)
    virtualenv_dir = "{0}/virtualenv".format(remote_dir)

    rsync_project(
        remote_dir=remote_dir,
        local_dir="./",
        exclude=("local_settings.py", "*.pyc", "*~", '._*', ".git",),
        delete=True,
        ssh_opts='-o StrictHostKeyChecking=no',
    )

    sed('{remote_dir}/sample/settings.py'.format(remote_dir=remote_dir), '__FABRIC_REVISION__', revision)

    run('/opt/python-3.5/bin/virtualenv {virtualenv_dir}'.format(
        virtualenv_dir=virtualenv_dir,
    ))

    run('{virtualenv_dir}/bin/pip install -r {remote_dir}/requirements.txt'.format(
        remote_dir=remote_dir,
        virtualenv_dir=virtualenv_dir,
    ))


def symlink():
    run('test -d {deploy_dir} && ln -snf {deploy_dir} {current_dir}'.format(
        deploy_dir="/var/apps/django-sample-app/releases/{0}".format(DEPLOY_VERSION),
        current_dir="/var/apps/django-sample-app/current",
    ))


def restart():
    uwsgi_pidfile = '/var/apps/django-sample-app/run/django-sample-app-uwsgi.pid'
    run('if test -f {uwsgi_pidfile}; then sudo -u deploy kill -HUP `cat {uwsgi_pidfile}`; fi'.format(uwsgi_pidfile=uwsgi_pidfile))


def supervisorctl(cmd, *args):
    arg = ' '.join(args)
    sudo('supervisorctl {cmd} {arg}'.format(cmd=cmd, arg=arg), shell=False)
