import os

from Code import flask_app
from flask_cors import CORS
import time

os.environ['TZ'] = 'Asia/Shanghai'
time.tzset()

app = flask_app.create_app()
CORS(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090, debug=True)
