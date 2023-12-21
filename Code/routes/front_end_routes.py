import os
from flask import Blueprint, send_from_directory

cur_path = os.getcwd()
build_folder_path = os.path.join(cur_path, "..", "chat_wsy", "build")

bp = Blueprint('front_end', __name__, static_url_path='')


def init_blueprint():
    @bp.route('/title/favicon.ico')
    def favicon():
        return send_from_directory(directory=os.path.join(build_folder_path, '..'), path='favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')

    @bp.route('/', defaults={'filename': ''})
    @bp.route('/<path:filename>')
    def serve(filename):
        if filename and os.path.exists(os.path.join(build_folder_path, filename)):
            return send_from_directory(build_folder_path, filename)
        else:
            return send_from_directory(build_folder_path, 'index.html')

        # 特定于 favicon.ico 的路由

    return bp
