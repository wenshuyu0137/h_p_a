from flask import Flask
from .routes import user_actions_routes, front_end_routes
from .mysql.mysql_init import DatabasePool
import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    # 创建日志记录器，指定日志级别
    logging.basicConfig(level=logging.INFO)

    # 创建一个日志文件处理器
    log_file_handler = RotatingFileHandler('agent_logs.log', maxBytes=10000000, backupCount=10)
    log_file_handler.setLevel(logging.INFO)

    # 创建日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file_handler.setFormatter(formatter)

    # 将文件处理器添加到日志记录器
    logging.getLogger().addHandler(log_file_handler)


class flask_app:
    def __init__(self):
        self.app = Flask(__name__)  # 创建Flask APP
        setup_logging()  # 初始化日志

        self.db_pool = DatabasePool()  # 初始化数据库 GPT的数据库

        self.app.register_blueprint(front_end_routes.init_blueprint())  # 前端
        self.app.register_blueprint(user_actions_routes.init_blueprint(self.db_pool))  # 初始化用户处理路由

    def get_app(self):
        return self.app


def create_app():
    my_app = flask_app()
    return my_app.get_app()
