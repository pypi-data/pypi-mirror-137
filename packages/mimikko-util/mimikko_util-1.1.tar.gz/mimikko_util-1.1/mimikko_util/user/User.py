import hashlib
from datetime import datetime
from json import dumps as json_dumps

import requests

from ..error import *
from .. import const_url


class User:
    """
    使用手机号/邮箱和密码方式登录的用户
    """
    def __init__(self, id: str, password: str) -> None:
        """
        :param id: 手机号/邮箱
        :param password: 密码
        """
        body = {
            "id": id,
            "password": hashlib.sha256(password.encode()).hexdigest()
        }
        r = requests.post(const_url.LOGIN, headers=const_url.HEADERS_WHEN_LOGIN,
                          data=json_dumps(body)).json()
        if r["code"] == "7":
            # 用户不存在
            raise UserNotFoundError(id)
        elif r["code"] == "8":
            # 密码不正确
            raise PasswordMismatchedError(id)
        # 登录成功
        # 获取Token字段，用于填充Authorization
        self._TOKEN = r["body"]["Token"]
        # 之后的请求都用这个header
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

    # region 更新缓存
    def update_all_cache(self) -> None:
        """
        更新所有缓存
        :return: None
        """
        self.update_user_info_cache()
        self.update_sign_status_cache()
        self.update_assistant_list_cache()
        self.update_assistant_detail_cache()

    def update_user_info_cache(self) -> None:
        """
        更新用户个人信息缓存
        :return: None
        """
        r = requests.get(const_url.USER_INFO, headers=self._HEADERS_AFTER_LOGIN).json()
        if r["code"] == "6":  # Token过期
            raise TokenOutdatedError(self._TOKEN)
        self._cache["user_info"] = r["body"]["Value"]

    def update_sign_status_cache(self) -> None:
        """
        更新签到状态缓存
        :return: None
        """
        r = requests.get(const_url.SIGN_STATUS, headers=self._HEADERS_AFTER_LOGIN).json()
        if r["code"] == "6":  # Token过期
            raise TokenOutdatedError(self._TOKEN)
        self._cache["sign_status"] = r["body"]

    def update_assistant_list_cache(self) -> None:
        """
        更新助手列表缓存
        :return: None
        """
        r = requests.get(const_url.ASSISTANT_LIST, headers=self._HEADERS_AFTER_LOGIN).json()
        if r["code"] == "6":  # Token过期
            raise TokenOutdatedError(self._TOKEN)
        for assistant in r["body"]["Items"]:
            self._cache["assistant_list"][assistant["code"]] = assistant

    def update_assistant_detail_cache(self) -> None:
        """
        更新助手详细信息
        :return: None
        """
        for assistant_code in self._cache["assistant_list"]:
            self.update_specific_assistant_detail_cache(assistant_code)

    def update_specific_assistant_detail_cache(self, assistant_code: str) -> None:
        """
        更新指定助手的详细信息
        :param assistant_code: 助手代号
        :return: None
        """
        r = requests.get(const_url.ASSISTANT_DETAIL.replace("{ASSISTANT_CODE}", assistant_code),
                         headers=self._HEADERS_AFTER_LOGIN).json()
        if r["code"] == "6":  # Token过期
            raise TokenOutdatedError(self._TOKEN)
        self._cache["assistant_detail"][assistant_code] = r["body"]
    # endregion

    # region 获取用户个人信息
    def get_user_id(self) -> str:
        """
        获取用户ID
        :return: None
        """
        return self._cache["user_info"]["UserId"]

    def get_user_name(self) -> str:
        """
        获取用户名
        :return: None
        """
        return self._cache["user_info"]["UserName"]

    def get_sex(self) -> str:
        """
        获取性别
        :return: None
        """
        return {
            1: "男",
            2: "女"
        }[self._cache["user_info"]["Sex"]]

    def get_birthday(self) -> datetime:
        """
        获取生日
        :return: None
        """
        raw = self._cache["user_info"]["Birthday"]
        return datetime.strptime(raw, "%Y-%m-%d")

    def get_level(self) -> int:
        """
        获取用户等级
        :return: None
        """
        return self._cache["user_info"]["Level"]

    def get_coin(self) -> int:
        """
        获取用户硬币数量
        :return: None
        """
        return self._cache["user_info"]["Coin"]

    def get_avatar_url(self) -> str:
        """
        获取用户头像Url
        :return: None
        """
        return self._cache["user_info"]["AvatarUrl"]
    # endregion

    # region 获取用户签到状态
    def get_is_signed(self) -> bool:
        """
        判断用户是否签到
        :return: bool
        """
        return self._cache["sign_status"]["IsSign"]

    def get_continuous_sign_days(self) -> int:
        """
        获取连续签到的天数
        :return: int
        """
        return self._cache["sign_status"]["ContinuousSignDays"]
    # endregion

    # region 获取签到信息
    def get_sign_motto_source(self) -> str:
        """
        获取签到的格言的出处
        :return: str
        """
        # 如果未签到或签到信息没有缓存，则进行签到
        if (not self.get_is_signed()) or (not self._cache["sign_info"]):
            self.do_sign()
        return self._cache["sign_info"]["Name"]

    def get_sign_motto(self) -> str:
        """
        获取签到的格言
        :return: str
        """
        # 如果未签到或签到信息没有缓存，则进行签到
        if (not self.get_is_signed()) or (not self._cache["sign_info"]):
            self.do_sign()
        return self._cache["sign_info"]["Description"]

    def get_sign_picture_url(self) -> str:
        """
        获取签到的背景图片
        :return: str
        """
        # 如果未签到或签到信息没有缓存，则进行签到
        if (not self.get_is_signed()) or (not self._cache["sign_info"]):
            self.do_sign()
        return self._cache["sign_info"]["PictureUrl"]

    def get_sign_reward(self) -> int:
        """
        获取签到的好感度
        :return:
        """
        # 如果未签到或签到信息没有缓存，则进行签到
        if (not self.get_is_signed()) or (not self._cache["sign_info"]):
            self.do_sign()
        return self._cache["sign_info"]["Reward"]
    # endregion

    # region 获取助手信息
    def get_assistant_count(self) -> int:
        """
        获取拥有的助手数量
        :return: int
        """
        return self._cache["assistant_list"]["Total"]

    def get_all_assistant_codes(self) -> set:
        """
        获取拥有的所有助手的代号
        返回如{"momona", "miruku2"}
        :return: set
        """
        return set(self._cache["assistant_list"].keys())

    def get_all_assistant_names(self) -> set:
        """
        获取拥有的所有助手的名称
        返回如{"梦梦奈", "米露可"}
        :return: set
        """
        return {a["ServantName"] for a in self._cache["assistant_list"].values()}

    def get_name_by_assistant_code(self, assistant_code: str) -> str:
        """
        根据助手代号获取助手名称
        :param assistant_code: 助手代号
        :return: str
        """
        return self._cache["assistant_list"][assistant_code]["ServantName"]

    def get_code_by_assistant_name(self, assistant_name: str) -> str:
        """
        根据助手名称获取助手代号
        :param assistant_name: 助手名称
        :return:
        """
        return next(k for k, v in self._cache["assistant_list"].items()
                    if v["ServantName"] == assistant_name)

    def get_default_assistant_code(self) -> str:
        """
        获取默认的助手的代号
        :return: str
        """
        return next(k for k, v in self._cache["assistant_list"].items() if v["IsDefault"])

    def get_image_by_assistant_code(self, assistant_code: str) -> str:
        """
        获取助手的图片Url
        :param assistant_code: 助手代号
        :return: str
        """
        return next(v["ServantImageUrl"] for v in self._cache["assistant_list"].values()
                    if v["ServantName"] == assistant_code)

    def get_assistant_favorability(self, assistant_code: str) -> int:
        """
        获取助手的好感度
        :param assistant_code: 助手代号
        :return: int
        """
        return self._cache["assistant_detail"][assistant_code]["Favorability"]

    def get_assistant_max_favorability(self, assistant_code: str) -> int:
        """
        获取助手好感度最大值
        :param assistant_code: 助手大小
        :return: int
        """
        return self._cache["assistant_detail"][assistant_code]["MaxFavorability"]

    def get_assistant_level(self, assistant_code: str) -> int:
        """
        获取助手等级
        :param assistant_code: 助手代号
        :return: int
        """
        return self._cache["assistant_detail"][assistant_code]["Level"]

    def get_assistant_level_description(self, assistant_code: str) -> int:
        """
        获取助手等级描述
        :param assistant_code: 助手代号
        :return: int
        """
        return self._cache["assistant_detail"][assistant_code]["LevelDescription"]

    def get_assistant_energy(self, assistant_code: str) -> int:
        """
        获取助手能量值
        :param assistant_code: 助手代号
        :return: int
        """
        return self._cache["assistant_detail"][assistant_code]["Energy"]

    def get_assistant_max_energy(self, assistant_code: str) -> int:
        """
        获取助手最大能量值（能量槽）
        :param assistant_code: 助手代号
        :return: int
        """
        return self._cache["assistant_detail"][assistant_code]["MaxEnergy"]
    # endregion

    # region 用户操作
    def do_sign(self) -> None:
        """
        每日签到
        :return: None
        """
        # 不管怎样都先签到
        r = requests.get(const_url.DO_SIGN, headers=self._HEADERS_AFTER_LOGIN).json()
        if r["code"] == "6":  # Token过期
            raise TokenOutdatedError(self._TOKEN)
        # 更新签到信息缓存
        self._cache["sign_info"] = r["body"]
        # 更新一下用户签到状态缓存
        self.update_sign_status_cache()
        # 更新助手详细信息
        self.update_assistant_detail_cache()

    def do_exchange_reward(self, assistant_code: str) -> None:
        """
        兑换助手能量值
        :param assistant_code: 助手代号，例如梦梦奈是momona
        :return: None
        """
        r = requests.get(const_url.DO_EXCHANGE_REWARD.replace("{ASSISTANT_CODE}", assistant_code),
                         headers=self._HEADERS_AFTER_LOGIN).json()
        if r["code"] == "6":  # Token过期
            raise TokenOutdatedError(self._TOKEN)
        elif r["code"] == "000316":  # 能量值不足
            raise NoEnoughRewardError()
        elif r["code"] == "5":  # 传参错误
            raise ArgumentError()
        # 更新助手详细信息
        self.update_assistant_detail_cache()
    # endregion
