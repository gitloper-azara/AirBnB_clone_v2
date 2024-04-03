#!/usr/bin/python3
'''A Fabric script that generates and distributes a .tgz archive
to webservers
'''
from os.path import exists
from fabric.api import local, env, put, run
from datetime import datetime

env.hosts = ['52.91.147.223', '18.210.33.113']
env.user = 'ubuntu'


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
    if res.succeeded:  # type: ignore
        # return path to the archive
        return f'versions/{archive_name}'
    else:
        return None


def do_deploy(archive_path):
    '''Distributes an archive to web servers'''
    # check if the archive file exists
    if not exists(archive_path):
        return False

    # extract the filename from the archhive path
    filename = archive_path.split('/')[-1]
    folder_name = filename.split('.')[0]

    # store directory paths in varibales
    releases_dir = '/data/web_static/releases/'
    current_dir = '/data/web_static/current'

    # upload the archive to the /tmp/ directory of the webservers
    put(archive_path, '/tmp/')

    # create the directory to uncompress the archive
    run(f'mkdir -p {releases_dir}{folder_name}')

    # uncompress the archive
    run(f'tar -xzf /tmp/{filename} -C {releases_dir}{folder_name}')

    # delete the archive from the webservers
    run(f'rm /tmp/{filename}')

    run(f'mv {releases_dir}{folder_name}/web_static/* '
        f'{releases_dir}{folder_name}')

    # delete redud directory
    run(f'rm -rf {releases_dir}{folder_name}/web_static')

    # delete the symbolic link
    run(f'rm -rf {current_dir}')

    # create a new symbolic link linked to the new version of code
    run(f'ln -s {releases_dir}{folder_name}/ {current_dir}')

    # return true if all operations are done correctly
    print('New version deployed!')
    return True


def deploy():
    '''Creates and distributes an archive to stated webservers,
    unarchives the archive and deploys the content
    '''
    # store the path of the created archive in a variable
    created_archive_path = do_pack()

    # return false if no archive has been created
    if not created_archive_path:
        return False

    # using the new path of the new archive, call the do_deploy() function
    return do_deploy(created_archive_path)
