Apache + mod-wsgi configuration
===============================

An example Apache2 vhost configuration follows::

    WSGIDaemonProcess hotelbooking-<target> threads=5 maximum-requests=1000 user=<user> group=staff
    WSGIRestrictStdout Off

    <VirtualHost *:80>
        ServerName my.domain.name

        ErrorLog "/srv/sites/hotelbooking/log/apache2/error.log"
        CustomLog "/srv/sites/hotelbooking/log/apache2/access.log" common

        WSGIProcessGroup hotelbooking-<target>

        Alias /media "/srv/sites/hotelbooking/media/"
        Alias /static "/srv/sites/hotelbooking/static/"

        WSGIScriptAlias / "/srv/sites/hotelbooking/src/hotelbooking/wsgi/wsgi_<target>.py"
    </VirtualHost>


Nginx + uwsgi + supervisor configuration
========================================

Supervisor/uwsgi:
-----------------

.. code::

    [program:uwsgi-hotelbooking-<target>]
    user = <user>
    command = /srv/sites/hotelbooking/env/bin/uwsgi --socket 127.0.0.1:8001 --wsgi-file /srv/sites/hotelbooking/src/hotelbooking/wsgi/wsgi_<target>.py
    home = /srv/sites/hotelbooking/env
    master = true
    processes = 8
    harakiri = 600
    autostart = true
    autorestart = true
    stderr_logfile = /srv/sites/hotelbooking/log/uwsgi_err.log
    stdout_logfile = /srv/sites/hotelbooking/log/uwsgi_out.log
    stopsignal = QUIT

Nginx
-----

.. code::

    upstream django_hotelbooking_<target> {
      ip_hash;
      server 127.0.0.1:8001;
    }

    server {
      listen :80;
      server_name  my.domain.name;

      access_log /srv/sites/hotelbooking/log/nginx-access.log;
      error_log /srv/sites/hotelbooking/log/nginx-error.log;

      location /500.html {
        root /srv/sites/hotelbooking/src/hotelbooking/templates/;
      }
      error_page 500 502 503 504 /500.html;

      location /static/ {
        alias /srv/sites/hotelbooking/static/;
        expires 30d;
      }

      location /media/ {
        alias /srv/sites/hotelbooking/media/;
        expires 30d;
      }

      location / {
        uwsgi_pass django_hotelbooking_<target>;
      }
    }
