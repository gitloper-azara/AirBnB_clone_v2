#!/usr/bin/env bash
# this bash script sets up webservers for the deployment of web_static content

# install nginx if not already installed
apt-get update
apt-get install -y nginx

# create directories, if they do not already exist
mkdir /data/
mkdir /data/web_static/
mkdir /data/web_static/shared/
mkdir /data/web_static/releases/
mkdir /data/web_static/releases/test/

# create a fake html file
touch /data/web_static/releases/test/index.html

# include simple content to test Nginx configuration
echo "<html>
<head><title>Hello World</title></head>
<body><h1>Hello World! Simple Content...</h1></body>
</html>" > /data/web_static/releases/test/index.html

# create symbolic link to stated directory
if [ -L /data/web_static/current ]; then
    rm /data/web_static/current
fi
ln -s /data/web_static/releases/test/ /data/web_static/current

# set recursive ownership of /data/ folder and its content to ubuntu user and group
chown -R ubuntu:ubuntu /data/

# define config data
config_data="/^server {/a \\\n\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t\tautoindex off;\n\t}"
# define config file path
config_file="/etc/nginx/sites-available/default"

# check if config block is not already within config file
grep -qF "$config_data" "$config_file"
status=$?
if [[ status -ne 0 ]]; then
    # if config data does not exist, exit status == 1, then...
    sed -i "$config_data" "$config_file"
else
    # otherwise...
    echo "Configuration exists!"
fi

# restart nginx service
service nginx restart
