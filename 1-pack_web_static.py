#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB Clone repo """

import time
from fabric.api import local
from os.path import exists


def do_pack():
    """ generates a .tgz archive from the contents of the web_static folder
    and stores archives in folder versions """

    now = time.strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{:s}.tgz".format(now)

    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static/".format(archive_path))
    if result.succeeded:
        return archive_path
    else:
        return None
