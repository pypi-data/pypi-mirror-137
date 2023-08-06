from .User import User
from .. import const_url


class TokenUser(User):
    """
    使用Token创建用户
    """
    def __init__(self, token: str) -> None:
        """
        :param token: 传入用户的Token
        """
        self._TOKEN = token
        self._HEADERS_AFTER_LOGIN = const_url.HEADERS_AFTER_LOGIN.copy()
        self._HEADERS_AFTER_LOGIN["Authorization"] = self._TOKEN
        # 设置缓存
        self._cache = {
            "user_info": {},  # 用户个人信息
            "sign_status": {},  # 用户签到状态(是否已签到、连续签到天数)
            "assistant_list": {},  # 助手列表，格式{代号: 基本信息}
            "assistant_detail": {},  # 助手详细信息，格式{代号: 详细信息}
            # 签到信息（今日签到卡片），但不由update_all_cache()控制
            # 必须先执行do_sign()才能获取今日签到卡片，不管是否已经签到了
            "sign_info": {},
        }
        # 更新所有缓存
        self.update_all_cache()
