import os
from flask import Blueprint, send_from_directory
import logging

cur_path = os.getcwd()
build_folder_path = "/home/lighthouse/h_p_a/front_end/build"

bp = Blueprint('agent_front_end', __name__, static_url_path='')


def init_blueprint():
    @bp.route('/title/favicon.ico')
    def favicon():
        return send_from_directory(directory=os.path.join(build_folder_path, '..'), path='favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')

    @bp.route('/', defaults={'filename': ''})
    @bp.route('/<path:filename>')
    def serve(filename):
        logging.info(os.path.join(build_folder_path, filename))
        if filename and os.path.exists(os.path.join(build_folder_path, filename)):
            return send_from_directory(build_folder_path, filename)
        else:
            return send_from_directory(build_folder_path, 'index.html')

    return bp
