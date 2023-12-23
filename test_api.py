import json
import time

import requests

'''
顶级代理
INSERT INTO Agent_Users (username, email, password, phone, invite_code, user_type, boss_agent_id, boss_agent_name) 
VALUES ('wenshuyu', 'wsy2161826815@163.com', '7d5524963320d977259087caaddd7001684dfc80c3ca3f34938bb249a105d471', '15616302420', '92e42f41cb2d4fece3c480448c62b6655ecf07c5cdb9379c1f5455c7d9dd4860', 0, 1, '');

充值
UPDATE Agent_Users SET balance=100 WHERE username="wenshuyu";
'''


class Agent:
    def __init__(self):
        # self.host_url = 'https://www.wenshuyu.chat/'
        self.host_url = "http://170.106.187.38:9000/"
        self.user_token = {
            "token": ""
        }
        self.username = ""
        self.boss = ''
        self.level = None
        self.invite_code = ''

    def send_email_code(self, username: str, email: str):
        cur_url = 'api/agent/email_code'
        args = {
            "username": username,
            "email": email
        }
        try:
            response = requests.post(url=self.host_url + cur_url, json=args)
            data = json.loads(response.text)
            return data
        except (json.decoder.JSONDecodeError, requests.exceptions.ConnectionError) as e:

            return None  # "网络连接异常"

    def agent_register(self, username, password, phone, email, email_code, boss_invite_code):
        cur_url = 'api/agent/register'
        args = {
            "username": username,
            "password": password,
            "phone": phone,
            "email": email,
            "email_code": f'{email_code}-{int(time.time())}',  # 注册验证码
            "boss_invite_code": boss_invite_code,  # 邀请码
        }
        try:
            response = requests.post(url=self.host_url + cur_url, json=args)
            data = json.loads(response.text)
            return data
        except (json.decoder.JSONDecodeError, requests.exceptions.ConnectionError):
            return None  # "网络连接异常"

    def agent_change_password(self, username: str, password: str, email_code: str):  # 注册
        cur_url = 'api/agent/change_pwd'
        args = {
            "username": username,
            "password": password,
            "email_code": f'{email_code}-{int(time.time())}'  # 注册验证码
        }
        try:
            response = requests.post(url=self.host_url + cur_url, json=args)
            data = json.loads(response.text)
            return data
        except (json.decoder.JSONDecodeError, requests.exceptions.ConnectionError) as e:

            return None  # "网络连接异常"

    def agent_login(self, username, password):
        cur_url = 'api/agent/login'
        args = {
            "username": username,
            "password": password
        }
        try:
            response = requests.post(url=self.host_url + cur_url, json=args)
            data = json.loads(response.text)
            if data["code"] == 0:
                self.user_token["token"] = data["token"]
                self.username = username

                other_info = self.agent_get_info()
                self.boss = other_info["message"][9]
                self.level = other_info["message"][7]
                self.invite_code = other_info["message"][1]

                return True
            return False
        except (json.decoder.JSONDecodeError, requests.exceptions.ConnectionError) as e:
            return None  # "网络连接异常"

    def agent_get_info(self):
        cur_url = 'api/agent/info'
        args = {
            "username": self.username,
        }
        try:
            response = requests.post(url=self.host_url + cur_url, json=args, headers=self.user_token)
            data = json.loads(response.text)
            return data
        except (json.decoder.JSONDecodeError, requests.exceptions.ConnectionError) as e:
            return None  # "网络连接异常"

    def agent_transaction(self, to_username: str, quantity: int, transaction_type: int):  # 分配0,赠送1
        cur_url = 'api/agent/transaction'
        args = {
            "from_username": self.username,
            "to_username": to_username,
            "quantity": quantity,
            "transaction_type": transaction_type
        }
        try:
            response = requests.post(url=self.host_url + cur_url, json=args, headers=self.user_token)
            data = json.loads(response.text)
            return data
        except (json.decoder.JSONDecodeError, requests.exceptions.ConnectionError) as e:
            return None  # "网络连接异常"

    def get_transaction_out(self):  # 卖出的交易
        cur_url = 'api/agent/get_trans_b_s'
        args = {
            "sender_name": self.username,
        }
        try:
            response = requests.post(url=self.host_url + cur_url, json=args, headers=self.user_token)
            data = json.loads(response.text)
            return data
        except (json.decoder.JSONDecodeError, requests.exceptions.ConnectionError) as e:
            return None  # "网络连接异常"

    def get_transaction_in(self):  # 进入的交易
        cur_url = 'api/agent/get_trans_b_r'
        args = {
            "receiver_name": self.username,
        }
        try:
            response = requests.post(url=self.host_url + cur_url, json=args, headers=self.user_token)
            data = json.loads(response.text)
            return data
        except (json.decoder.JSONDecodeError, requests.exceptions.ConnectionError) as e:
            return None  # "网络连接异常"

    def create_redeem(self, quantity: int):  # 创建兑换码
        cur_url = 'api/agent/create_redeem'
        args = {
            "username": self.username,
            "quantity": quantity,
        }
        try:
            response = requests.post(url=self.host_url + cur_url, json=args, headers=self.user_token)
            data = json.loads(response.text)
            return data
        except (json.decoder.JSONDecodeError, requests.exceptions.ConnectionError) as e:
            return None  # "网络连接异常"

    def get_redeem(self):  # 创建兑换码
        cur_url = 'api/agent/get_redeem'
        args = {
            "username": self.username,
        }
        try:
            response = requests.post(url=self.host_url + cur_url, json=args, headers=self.user_token)
            data = json.loads(response.text)
            return data
        except (json.decoder.JSONDecodeError, requests.exceptions.ConnectionError) as e:
            return None  # "网络连接异常"

    def delete_redeem(self, code_id: int):  # 创建兑换码
        cur_url = 'api/agent/delete_redeem'
        args = {
            "code_id": code_id,
        }
        try:
            response = requests.post(url=self.host_url + cur_url, json=args, headers=self.user_token)
            data = json.loads(response.text)
            return data
        except (json.decoder.JSONDecodeError, requests.exceptions.ConnectionError) as e:
            return None  # "网络连接异常"


u = "wenshuyu"
p = "2161826815www"
i_code = "92e42f41cb2d4fece3c480448c62b6655ecf07c5cdb9379c1f5455c7d9dd4860"
a = Agent()
a.agent_login(u, p)
ret = a.create_redeem(20)  # 不是人民币,是点数
# ret = a.get_redeem()
print(ret)
# 832a8801515ae654041d84d139fce6f79b23f2fe43c7e13f749094fbd4ddc3a9
