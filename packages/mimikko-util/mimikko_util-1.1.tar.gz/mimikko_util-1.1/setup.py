from setuptools import setup, find_packages


setup(
    name="mimikko_util",
    version="1.01",
    description="兽耳助手非官方模块，用于用户签到、能量值兑换、查询等操作",
    long_description="""
mimikko_util

简介
兽耳助手非官方模块，用于用户签到、能量值兑换、查询等操作  
由于考虑到主要受众为中国用户，故模块注释和文档均采用中文  
项目托管也使用国内的Gitee  

使用方法
使用方法请参考项目Wiki
链接：https://gitee.com/MrDeveloper123/mimikko_util/wikis

项目链接
https://gitee.com/MrDeveloper123/mimikko_util

pypi链接
https://pypi.org/project/mimikko-util/
""",
    author="MrDeveloper123",
    author_email="mrdeveloper123@outlook.com",
    license="Apache-2.0",
    platforms=["all"],
    url="https://gitee.com/MrDeveloper123/mimikko_util",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    python_requires=">=3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
    ],
)
