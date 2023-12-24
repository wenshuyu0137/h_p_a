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
[Unit]
Description=Gunicorn instance to serve gpt_server
After=network.target

[Service]
WorkingDirectory=/home/lighthouse/h_p_a
ExecStart=sudo gunicorn --workers 12 --timeout=150 --bind 0.0.0.0:8100 init:app

[Install]
WantedBy=multi-user.target
'''
