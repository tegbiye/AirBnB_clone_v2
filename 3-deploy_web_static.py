#!/usr/bin/python3
# a Fabric script that generates a .tgz archive
# from the contents of web_static
import os.path
from fabric.api import *
from fabric.contrib import files
import os.path
from datetime import datetime


def do_pack():
    """do pack script for compressing
    """
    local('mkdir -p versions')
    str_date = datetime.now().strftime('%Y%m%d%H%M%S')
    path = 'versions/web_static_{}.tgz'.format(str_date)
    check = local('tar -cvzf {} web_static'.format(path))

    if check.failed:
        return None

    else:
        return path

env.user = "ubuntu"
env.hosts = ['104.196.182.248', '3.95.214.115']


def do_deploy(archive_path):
    """ Transfers archive_path to web servers above
    """
    if not os.path.isfile(archive_path):
        return False

    basename = os.path.basename(archive_path)
    root, ext = os.path.splitext(basename)
    target = '/data/web_static/releases/{}'.format(root)

    try:
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}/".format(target))
        run("sudo tar -xzf /tmp/{} -C {}/".format(basename, target))
        run("sudo rm /tmp/{}".format(basename))
        run("sudo mv {}/web_static/* {}/".format(target, target))
        run("sudo rm -rf {}/web_static".format(target))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(target))
        print('New version uploaded!')

    except:
        return False

    else:
        return True


def deploy():
    """
    Fabric script (based on the file 2-do_deploy_web_static.py) that creates
    and distributes an archive to your web servers, using the function deploy
    """

    filepath = do_pack()

    if filepath is None:
        return False

    return do_deploy(filepath)
