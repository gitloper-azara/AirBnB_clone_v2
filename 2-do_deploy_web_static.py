#!/usr/bin/python3
from fabric.api import env, run, put
from os.path import exists

env.hosts = ['52.91.147.223', '18.210.33.113']
env.user = 'ubuntu'


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
