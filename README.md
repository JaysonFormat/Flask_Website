# Flask_Website
 Legit Flask Website

# Don't Forget
# 'CREATE ANOTHER USER FOR DATABASE AND GRANT ALL PRIVILEGES
# 'sudo ufw allow http/tcp'
# gunicorn --workers=3 run:app'
# Don't forget to change the file size accepted in nginx
- client_max_body_size 8M;
# Don't Forger to change the timezone in linux Asia/Manila
# Don't Forget to change the API keys and payment_successful redirects

Supervisor /etc/supervisor/conf.d/flask_app.conf

[program:flask_app]
directory=/root/Flask_Website
command=gunicorn3 --workers=3 run:app
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/flask_app/flask_app.err.log
stdout_logfile=/var/log/flask_app/flask_app.out.log
