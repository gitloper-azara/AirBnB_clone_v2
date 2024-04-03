#!/usr/bin/python3

from fabric.api import local
from datetime import datetime


def do_pack():
    '''Generates a .tgz archive from the contents of teh web_static
    folder
    '''
    # generate or create the versions directory if not exists
    local('mkdir -p versions')

    # get current datetime
    date_time = datetime.now().strftime('%Y%m%d%H%M%S')

    # set the name of archive
    archive_name = f'web_static_{date_time}.tgz'

    # compress contents of the web_static folder into archive
    res = local(f'tar -cvzf versions/{archive_name} web_static')

    # check if compression was a success
    if res.succeeded: # type: ignore
        # return path to the archive
        return f'versions/{archive_name}'
    else:
        return None
