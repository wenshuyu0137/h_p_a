import hashlib
import time


def generate_full_invite_code(username):  #生成邀请码
    # 获取当前时间戳
    timestamp = str(int(time.time()))

    # 结合用户名和时间戳
    combined = username + timestamp

    # 使用SHA-256哈希算法生成完整的哈希值
    hash_result = hashlib.sha256(combined.encode()).hexdigest()

    return hash_result


def generate_redeem(username: str, number: int):  # 生成兑换码
    # 获取当前时间的时间戳
    timestamp = int(time.time())

    # 将用户名、数字和时间戳组合
    combined_input = f"{username}{number}{timestamp}"

    # 使用SHA-256哈希算法生成哈希值
    hash_result = hashlib.sha256(combined_input.encode()).hexdigest()

    return hash_result
