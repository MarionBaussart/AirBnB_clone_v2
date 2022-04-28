#!/usr/bin/python3
""" Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy """
from fabric.api import put, run, env
from os.path import exists

env.hosts = ['35.237.22.35', '35.237.118.104']


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
