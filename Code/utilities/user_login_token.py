import jwt
import datetime
from jwt.exceptions import ExpiredSignatureError


class login_token_func:
    _SECRET_KEY = 'GPT_USER_TOKEN'

    def generate_token(self, username: str):
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        return jwt.encode({'username': username, 'exp': expiration_time}, self._SECRET_KEY, algorithm='HS256')

    def validate_token(self, received_token):
        try:
            jwt.decode(received_token, self._SECRET_KEY, algorithms=['HS256'])
            return 0
        except ExpiredSignatureError:
            return -1  # 过期
        except jwt.InvalidTokenError:
            return -2  # 无效
