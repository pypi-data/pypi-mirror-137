class UserNotFoundError(Exception):
    """
    用户不存在
    """
    def __init__(self, id: str) -> None:
        self.id = id

    def __str__(self) -> str:
        return f"用户{self.id}不存在"


class PasswordMismatchedError(Exception):
    """
    密码错误
    """
    def __init__(self, id: str) -> None:
        self.id = id

    def __str__(self) -> str:
        return f"密码与用户f{self.id}不匹配"


class TokenOutdatedError(Exception):
    """
    Token过期，鉴权失败
    """
    def __init__(self, token: str):
        self.token = token

    def __str__(self) -> str:
        return f"用户Token {self.token} 已失效，请重新登录"


class NoEnoughRewardError(Exception):
    """
    能量值不足，兑换失败
    """
    def __str__(self) -> str:
        return "用户能量值不足，兑换失败"


class ArgumentError(Exception):
    """
    传参错误
    """
    def __str__(self) -> str:
        return "传参错误"
