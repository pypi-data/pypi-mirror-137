from setuptools import setup, find_packages


setup(
    name="mimikko_util",
    version="1.2",
    description="兽耳助手非官方模块，用于用户签到、能量值兑换、查询等操作",
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
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
