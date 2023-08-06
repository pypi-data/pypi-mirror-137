"""
请求URL
"""

# region header
# 登录时的请求header
HEADERS_WHEN_LOGIN = {
    "Accept": "application/json",
    "Cache-Control": "no-cache",
    "AppId": "wjB7LOP2sYkaMGLC",
    "Version": "3.3.2",
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/3.12.1",
}

# 成功登录后的请求header，加入Authorization字段
# Authentication为成功登录后返回的用户Token
HEADERS_AFTER_LOGIN = HEADERS_WHEN_LOGIN.copy()
HEADERS_AFTER_LOGIN["Authorization"] = ""
# endregion

# region 查询
# 登录，*POST请求
# body为包含id和password的JSON，对应手机号/邮箱、SHA256密码
LOGIN = "https://api1.mimikko.cn/client/user/LoginWithPayload"

# 获取用户个人信息，GET请求
USER_INFO = "https://api1.mimikko.cn/client/user/GetUserOwnInformation"

# 用户签到状态，GET请求
SIGN_STATUS = "https://api1.mimikko.cn/client/user/GetUserSignedInformation"

# 助手列表，GET请求
ASSISTANT_LIST = "https://api1.mimikko.cn/client/Servant/GetServantList"

# 助手信息
# 需要替换{ASSISTANT_CODE}为对应助手的代号，例如momona（梦梦奈）、miruku2（米露可）
ASSISTANT_DETAIL = "https://api1.mimikko.cn/client/love/GetUserServantInstance?code={ASSISTANT_CODE}"
# endregion

# region 操作
# 兑换能量值，GET请求
# 需要替换{ASSISTANT_CODE}为对应助手的代号，例如momona（梦梦奈）、miruku2（米露可）
DO_EXCHANGE_REWARD = "https://api1.mimikko.cn/client/love/ExchangeReward?code={ASSISTANT_CODE}"

# 签到，GET请求
DO_SIGN = "https://api1.mimikko.cn/client/RewardRuleInfo/SignAndSignInformationV3"
# endregion
