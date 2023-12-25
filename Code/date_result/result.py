import logging


class OperationResult:
    def __init__(self, success, data=None, error=None):
        self.success = success
        self.data = data
        self.error = error


def create_failure_result(exception):
    error_msg = str(exception)
    logging.error(error_msg)  # 记录错误日志
    return OperationResult(success=False, error=error_msg)


class ErrorCode:
    # 所有的 -1 错误码为具体的异常捕获而产生的信息
    # 所有的 -2 错误码为相关接口返回的错误信息

    user_error_code = {
        -3: "用户不存在",
        -4: "密码错误",
        -5: "会话已过期，请重新登录",
        -6: "无效token",
        -7: "余额不足",
        -8: "用户已存在",
        -9: "邀请码错误",
        -10: "已超过最大代理级别"
    }

    email_error_code = {
        -3: "该邮箱已被注册",
        -4: "验证码错误"
    }

    public_error_code = {
        -3: "无效的参数"
    }

    redeem_error_code = {
        -3: "兑换码不存在",
        -4: "兑换码已失效"
    }
