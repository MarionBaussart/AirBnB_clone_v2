#!/usr/bin/python3
""" Fabric script (based on the file 2-do_deploy_web_static.py) that creates
and distributes an archive to your web servers, using the function deploy """

import time
from fabric.api import local, put, run, env
from os.path import exists, isdir
env.hosts = ['35.237.22.35', '35.237.118.104']


def do_pack():
    """ generates a .tgz archive from the contents of the web_static folder
    and stores archives in folder versions """
    try:
        now = time.strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir -p versions")
        file_name = "versions/web_static_{}.tgz".format(now)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    """ deploy archive """
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        """ Upload the archive to the /tmp/ directory of the web server """
        put(archive_path, '/tmp/')
        """ Uncompress the archive """
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        """ Delete the archive from the web server """
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        """ Delete the symbolic link """
        run('rm -rf /data/web_static/current')
        """ Create a new the symbolic link """
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except Exception:
        return False


def deploy():
    """ creates and distributes an archive to your web servers """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
