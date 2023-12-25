import json
import os
import random
from string import ascii_letters, digits
import requests
from flask import Blueprint, request, jsonify, send_from_directory
from ..date_result.result import *
from ..mysql.mysql_agent_users import AgentUsers
from ..mysql.mysql_init import DatabasePool
from ..mysql.mysql_email_code import EmailCode
from ..mysql.mysql_transactions import Transactions
from ..mysql.mysql_redeem_codes import RedeemCodes
from ..utilities.user_login_token import login_token_func
from ..utilities.generate_code import *

bp = Blueprint('user', __name__)


def send_email(des_email: str, subject: str):
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    timestamp = int(time.time())

    url = "https://luckycola.com.cn/tools/customMail"
    args = {
        "ColaKey": "ged2ufwKeTSYc81700811954802y30Tnn3tT3",
        "tomail": des_email,
        "fromTitle": "账号注册",
        "subject": subject,  # 邮件主题
        "content": f'"注册验证码码为{code}"',  # 文本内容
        "smtpCode": "UPMHVNAXCXREQWXS",
        "smtpEmail": "wsy2161826815@163.com",
        "smtpCodeType": "163"
    }
    try:
        ret = requests.post(url=url, json=args).text
        return OperationResult(success=True, data=(f"{code}-{timestamp}", json.loads(ret)))
    except Exception as e:
        return create_failure_result(e)


def is_verification_code_valid(user_db_code, user_client_code: str, valid_duration=120):
    try:
        db_code, db_timestamp = user_db_code.split('-')
        db_timestamp = int(db_timestamp)

        client_code, client_timestamp = user_client_code.split('-')
        client_timestamp = int(client_timestamp)
        # 检查验证码是否在有效时间内
        return db_code == client_code and client_timestamp - db_timestamp < valid_duration
    except ValueError:
        # 如果格式不正确，返回False
        return False


def generate_random_string(length):
    letters = ascii_letters + digits  # 包括字母和数字
    return ''.join(random.choice(letters) for _ in range(length))


def init_blueprint(db_pool: DatabasePool):
    user_table = AgentUsers(db_pool)
    email_code_table = EmailCode(db_pool)
    transactions_table = Transactions(db_pool)
    redeem_table = RedeemCodes(db_pool)

    def validate_user_token(token: str):
        token_validate = login_token_func().validate_token(token)
        if token_validate == -1:
            code = -5
            return jsonify({"code": code, "message": ErrorCode.user_error_code[code]})
        if token_validate == -2:
            code = -6
            return jsonify({"code": code, "message": ErrorCode.user_error_code[code]})
        return True

    def judge_user_exists(username: str):
        user_exit_flag = user_table.user_exists(username)
        if not user_exit_flag.success:
            return jsonify({"code": -1, "message": user_exit_flag.error})  # 这个错误由数据库操作捕获的异常产生
        return user_exit_flag.data

    cur_path = os.getcwd()
    build_folder_path = os.path.join(cur_path, "front_end", "build")

    @bp.route('/', defaults={'filename': ''})
    @bp.route('/<path:filename>')
    def serve(filename):
        print(os.path.join(build_folder_path, filename))
        if filename and os.path.exists(os.path.join(build_folder_path, filename)):
            return send_from_directory(build_folder_path, filename)
        else:
            return send_from_directory(build_folder_path, 'index.html')

    @bp.route('/say_hi', methods=['GET'])
    def say_hi():
        return json.dumps({"code": 0, "message": "hello world!"})

    @bp.route('/api/agent/validate_token', methods=['POST'])
    def validate_token():
        data = request.get_json()
        try:
            token = data['token']
        except KeyError:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.public_error_code[code]})  # 无效的参数

        token_validate = login_token_func().validate_token(token)
        info_dict = {
            0: "验证成功",
            -1: "token已过期",
            -2: "无效的token"
        }
        return jsonify({"code": token_validate, "message": info_dict[token_validate]})

    @bp.route('/api/agent/email_code', methods=['POST'])
    def proxy_send_email():  # 发送邮箱验证码
        data = request.get_json()
        try:
            username = data['username']
            email = data['email']
        except KeyError:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.public_error_code[code]})

        send_flag = send_email(email, "注册验证")
        if not send_flag.success:
            return jsonify({"code": -1, "message": send_flag.error})

        rand_code, data = send_flag.data
        if data["code"] == 0:
            get_flag = email_code_table.user_exists(username)
            if not get_flag.success:
                return jsonify({"code": -1, "message": get_flag.error})  # 这个错误由数据库操作捕获的异常产生
            if get_flag.data:
                update_flag = email_code_table.update_code(username, rand_code)
                if not update_flag.success:
                    return jsonify({"code": -1, "message": update_flag.error})  # 这个错误由数据库操作捕获的异常产生
            else:
                add_flag = email_code_table.add_code(username, rand_code)
                if not add_flag.success:
                    return jsonify({"code": -1, "message": add_flag.error})  # 这个错误由数据库操作捕获的异常产生
            return jsonify({"code": 0, "message": '发送成功'})
        else:
            return jsonify({"code": -2, "message": f'{data["msg"]}'})

    @bp.route('/api/agent/register', methods=['POST'])
    def register():
        data = request.get_json()
        try:
            username = data['username']
            password = data['password']
            phone = data['phone']
            email = data['email']
            client_email_code = data['email_code']
            boss_invite_code = data["boss_invite_code"]  # 上级的邀请码
        except KeyError:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.public_error_code[code]})

        ret = judge_user_exists(username)  # 用户名已存在
        if ret is True:
            code = -8
            return jsonify({"code": code, "message": ErrorCode.user_error_code[code]})

        exists_data = user_table.email_exists(email)  # 邮箱已被注册
        if not exists_data.success:
            return jsonify({"code": -1, "message": exists_data.error})  # 这个错误由数据库操作捕获的异常产生
        elif exists_data.data:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.email_error_code[code]})

        get_flag = email_code_table.query_code(username)  # 获取发送出去的验证码
        if not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})

        if not is_verification_code_valid(get_flag.data, client_email_code):  # 校验邮箱验证码
            code = -4
            return jsonify({"code": code, "message": ErrorCode.email_error_code[code]})

        delete_flag = email_code_table.delete_code(username)  # 删除验证码
        if not delete_flag.success:
            return jsonify({"code": -1, "message": delete_flag.error})

        get_flag = user_table.get_user_by_invite_code(boss_invite_code)  # 判断邀请码是否存在
        if get_flag is None:  # 邀请码不存在
            code = -9
            return jsonify({"code": code, "message": ErrorCode.user_error_code[code]})
        elif not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})

        boss_agent_id, user_type, boss_username = get_flag.data
        if user_type >= 3:
            code = -10
            return jsonify({"code": code, "message": ErrorCode.user_error_code[code]})  # 目前只支持三级代理

        self_invite_code = generate_full_invite_code(username)  # 创建自己的邀请码

        add_flag = user_table.create_user(username, email, password, phone, self_invite_code, user_type + 1,
                                          boss_agent_id, boss_username)
        if not add_flag.success:
            return jsonify({"code": -1, "message": add_flag.error})

        return jsonify({"code": 0, "message": '注册成功'})

    @bp.route('/api/agent/change_pwd', methods=['POST'])
    def change_pwd():
        data = request.get_json()
        try:
            username = data['username']
            password = data['password']
            client_email_code = data['email_code']
        except KeyError:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.public_error_code[code]})

        ret = judge_user_exists(username)
        if ret is not True:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.user_error_code[code]})

        get_flag = email_code_table.query_code(username)
        if not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})

        if is_verification_code_valid(get_flag.data, client_email_code):
            delete_flag = email_code_table.delete_code(username)
            if not delete_flag.success:
                return jsonify({"code": -1, "message": delete_flag.error})

            update_flag = user_table.update_password(username, password)
            if not update_flag.success:
                return jsonify({"code": -1, "message": update_flag.error})

            return jsonify({"code": 0, "message": '修改成功'})

        else:
            code = -4
            return jsonify({"code": code, "message": ErrorCode.email_error_code[code]})

    @bp.route('/api/agent/login', methods=['POST'])
    def login():
        data = request.get_json()
        try:
            username = data['username']
            password = data['password']
        except KeyError:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.public_error_code[code]})

        ret = judge_user_exists(username)
        if ret is not True:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.user_error_code[code]})  # 这个错误由数据库操作捕获的异常产生

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        get_flag = user_table.get_user_password(username)
        if not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})

        if get_flag.data[0] == password_hash:
            return jsonify(
                {"code": 0, "message": "登录成功", "token": f"{login_token_func().generate_token(username)}"})
        else:
            code = -4
            return jsonify({"code": code, "message": ErrorCode.user_error_code[code]})

    @bp.route('/api/agent/info', methods=['POST'])
    def get_info():
        data = request.get_json()
        try:
            username = data['username']
            user_token = request.headers["Token"]
        except KeyError:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.public_error_code[code]})

        user_token_check = validate_user_token(user_token)
        if user_token_check is not True:
            return user_token_check

        ret = judge_user_exists(username)
        if ret is not True:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.user_error_code[code]})

        get_flag = user_table.get_user_info(username)
        if not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})

        return jsonify({"code": 0, "message": get_flag.data})

    @bp.route('/api/agent/load_all_sub_agent', methods=['POST'])  # 获取自己的下级代理
    def load_all_sub_agent():
        data = request.get_json()
        try:
            username = data['username']
            user_token = request.headers["Token"]
        except KeyError:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.public_error_code[code]})

        user_token_check = validate_user_token(user_token)
        if user_token_check is not True:
            return user_token_check

        get_flag = user_table.get_all_sub_agent(username)  # 查表获取所有下级代理
        if not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})

        return jsonify({"code": 0, "message": get_flag.data})

    @bp.route('/api/agent/transaction', methods=['POST'])  # 发起HP点的交易
    def transaction():
        data = request.get_json()
        try:
            from_username = data['from_username']
            to_username = data['to_username']
            quantity = data["quantity"]
            transaction_type = data["transaction_type"]  # 分配0,赠送1
            user_token = request.headers["Token"]
        except KeyError:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.public_error_code[code]})

        user_token_check = validate_user_token(user_token)
        if user_token_check is not True:
            return user_token_check

        get_flag = user_table.get_user_balance(from_username)
        if not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})

        from_username_remain = get_flag.data[0]  # 点数不足
        if from_username_remain < quantity:
            code = -7
            return jsonify({"code": code, "message": ErrorCode.user_error_code[code]})

        get_flag = user_table.get_user_balance(to_username)  # 目标点数
        if not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})
        to_username_remain = get_flag.data[0]

        from_username_remain -= quantity
        to_username_remain += quantity
        update_flag = user_table.update_balance(from_username, from_username_remain)  # 减余额
        if not update_flag.success:
            return jsonify({"code": -1, "message": update_flag.error})
        update_flag = user_table.update_balance(to_username, to_username_remain)  # 加余额
        if not update_flag.success:
            return jsonify({"code": -1, "message": update_flag.error})

        get_flag = user_table.get_id_by_username(from_username)  # 获取来源ID
        if not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})
        from_id = get_flag.data[0]

        get_flag = user_table.get_id_by_username(to_username)  # 获取目标ID
        if not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})
        to_id = get_flag.data[0]

        add_flag = transactions_table.create_transaction(from_id, from_username, to_id, to_username, quantity,
                                                         transaction_type)
        if not add_flag.success:
            return jsonify({"code": -1, "message": add_flag.error})

        return jsonify({"code": 0, "message": '交易成功'})

    @bp.route('/api/agent/get_trans_b_s', methods=['POST'])
    def get_transaction_by_sender():
        data = request.get_json()
        try:
            sender_name = data['sender_name']
            user_token = request.headers["Token"]
        except KeyError:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.public_error_code[code]})

        user_token = validate_user_token(user_token)
        if user_token is not True:
            return user_token

        get_flag = transactions_table.get_transaction_by_sender(sender_name)
        if not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})
        record = get_flag.data

        return jsonify({"code": 0, "message": '', "record": record})

    @bp.route('/api/agent/get_trans_b_r', methods=['POST'])
    def get_transaction_by_receiver():
        data = request.get_json()
        try:
            receiver_name = data['receiver_name']
            user_token = request.headers["Token"]
        except KeyError:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.public_error_code[code]})

        user_token = validate_user_token(user_token)
        if user_token is not True:
            return user_token

        get_flag = transactions_table.get_transaction_by_reciever(receiver_name)
        if not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})
        record = get_flag.data

        return jsonify({"code": 0, "message": '', "record": record})

    @bp.route('/api/agent/create_redeem', methods=['POST'])  # 创建兑换码
    def create_redeem():
        data = request.get_json()
        try:
            username = data['username']
            quantity = data['quantity']  # 金额
            user_token = request.headers["Token"]
        except KeyError:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.public_error_code[code]})

        user_token = validate_user_token(user_token)
        if user_token is not True:
            return user_token

        get_flag = user_table.get_user_balance(username)
        if not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})

        username_remain = get_flag.data[0]  # 点数不足
        if username_remain < quantity:
            code = -7
            return jsonify({"code": code, "message": ErrorCode.user_error_code[code]})
        username_remain -= quantity

        update_flag = user_table.update_balance(username, username_remain)  # 数据库减余额
        if not update_flag.success:
            return jsonify({"code": -1, "message": update_flag.error})

        redeem_code = generate_redeem(username, quantity)  # 生成兑换码

        get_flag = user_table.get_id_by_username(username)  # 获取ID
        if not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})
        self_id = get_flag.data[0]

        add_flag = redeem_table.create_redeem_code(redeem_code, quantity, self_id, username)  # 添加兑换码到数据库
        if not add_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})

        return jsonify({"code": 0, "message": '创建成功'})

    @bp.route('/api/agent/get_redeem', methods=['POST'])  # 获取代理拥有的兑换码
    def get_redeem():
        data = request.get_json()
        try:
            username = data['username']
            user_token = request.headers["Token"]
        except KeyError:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.public_error_code[code]})

        user_token = validate_user_token(user_token)
        if user_token is not True:
            return user_token

        get_flag = redeem_table.get_redeem_code(username)  # 获取兑换码
        if not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})

        return jsonify({"code": 0, "message": get_flag.data})

    @bp.route('/api/agent/undoRedeem', methods=['POST'])  # 删除兑换码
    def delete_redeem():
        data = request.get_json()
        try:
            username = data["username"]
            redeem_code = data['redeem_code']  # 兑换码ID
            user_token = request.headers["Token"]
        except KeyError:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.public_error_code[code]})

        user_token = validate_user_token(user_token)
        if user_token is not True:
            return user_token

        get_flag = redeem_table.get_redeem_by_code(redeem_code)
        if not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})

        if get_flag.data is None:
            code = -3
            return jsonify({"code": code, "message": ErrorCode.redeem_error_code[code]})  #兑换码不存在

        valid_code_flag = get_flag.data[5]  #是否被使用
        if not valid_code_flag:
            code = -4
            return jsonify({"code": code, "message": ErrorCode.redeem_error_code[code]})  #兑换码已被使用

        balance = get_flag.data[2]  #兑换码的值

        get_flag = user_table.get_user_balance(username)
        if not get_flag.success:
            return jsonify({"code": -1, "message": get_flag.error})

        username_remain = get_flag.data[0]

        new_remain = username_remain + balance  #返回金额

        update_flag = user_table.update_balance(username, new_remain)  #更新余额
        if not update_flag.success:
            return jsonify({"code": -1, "message": update_flag.error})

        delete_flag = redeem_table.delete_redeem_code(redeem_code)  # 删除兑换码
        if not delete_flag.success:
            return jsonify({"code": -1, "message": delete_flag.error})

        return jsonify({"code": 0, "message": '删除成功'})

    return bp
