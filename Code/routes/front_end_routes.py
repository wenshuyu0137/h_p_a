import os
from flask import Blueprint, send_from_directory

cur_path = os.getcwd()
build_folder_path = "/home/lighthouse/h_p_a/front_end/build"

bp = Blueprint('agent_front_end', __name__)


def init_blueprint():
    @bp.route('/', defaults={'filename': ''})
    @bp.route('/<path:filename>')
    def serve(filename):
        if filename and os.path.exists(os.path.join(build_folder_path, filename)):
            return send_from_directory(build_folder_path, filename)
        else:
            return send_from_directory(build_folder_path, 'index.html')

    return bp
