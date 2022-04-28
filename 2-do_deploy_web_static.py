#!/usr/bin/python3
""" Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy """

import time
from fabric.api import put, run, env
from os.path import exists
env.hosts = ['35.237.22.35', '35.237.118.104']


def do_deploy(archive_path):
    """ deploy archive """
    if exists(archive_path) is False:
        return False
    try:
        """ Upload the archive to the /tmp/ directory of the web server """
        put(archive_path, "/tmp/")

        """ Uncompress the archive to the folder
        /data/web_static/releases/<archive filename without extension>
        on the web server """
        name_file = archive_path.split("/")[-1]
        new_path = ("/data/web_static/releases/" + name_file.spilt(".")[0])
        run("mkdir -p {}/".format(new_path))
        run("tar -xzf /tmp/{} -C {}/".format(name_file, new_path))

        """ Delete the archive from the web server """
        run("rm /tmp/{}".format(name_file))
        run("mv {}/web_static/* {}/".format(new_path, new_path))
        run("rm -rf {}/web_static".format(new_path))

        """ Delete the symbolic link /data/web_static/current
        from the web server """
        run("rm -rf /data/web_static/current")

        """ Create a new the symbolic link /data/web_static/current
        on the web server, linked to the new version of your code
        (/data/web_static/releases/<archive filename without extension>) """
        run("ln -s {}/ /data/web_static/current".format(new_path))
        return True
    except Exception:
        return False
