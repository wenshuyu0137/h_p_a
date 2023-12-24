import os

from Code import flask_app
from flask_cors import CORS
import time

os.environ['TZ'] = 'Asia/Shanghai'
time.tzset()

app = flask_app.create_app()
CORS(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)

'''
location /agent {
    proxy_pass http://localhost:8100;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    client_max_body_size 50M;
    proxy_buffering off;
}


[Unit]
Description=Gunicorn instance to serve gpt_server
After=network.target

[Service]
WorkingDirectory=/home/lighthouse/h_p_a
ExecStart=sudo gunicorn --workers 12 --timeout=150 --bind 0.0.0.0:8100 init:app

[Install]
WantedBy=multi-user.target
'''
