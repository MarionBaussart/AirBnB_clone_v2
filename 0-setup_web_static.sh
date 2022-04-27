#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static

# install Nginx
apt update
apt install nginx -y
service nginx restart

# create folders (-p create parent if doesn't exists)
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

# create HTML file to test Nginx config
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# create a symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group
chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of
# /data/web_static/current/ to hbnb_static
sed -i "/server_name _;/a\        location /hbnb_static {\n            alias /data/web_static/current;\n        }" /etc/nginx/sites-available/default
service nginx restart
