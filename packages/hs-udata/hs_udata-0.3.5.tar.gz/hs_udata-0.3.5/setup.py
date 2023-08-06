import os
from setuptools import setup,find_packages

path = os.path.abspath(os.path.dirname(__file__))

try:
  with open(os.path.join(path, 'README.md')) as f:
    long_description = f.read()
except Exception as e:
    long_description = "hs_udata from hundsun"

setup(
    name = "hs_udata",
    version = "0.3.5",
    long_description = long_description,
    python_requires=">=3.0.0",
    license = "MIT Licence",

    url = "https://udata.hs.net/home?channel_source=pypi",
    author = "恒生Light云",
    author_email = "huhl37814@hundsun.com",
    description=u'恒有数，源自恒生电子的金融数据社区，提供涵盖股票、基金、债券、期权期货、港股等金融数据；提供在线预览、在线下载和在线调试等功能，提供简单高效的API接口（接口语言包括HTTP、Python、MATLAB、Java）；提供丰富的接口文档、帮助文档与社区社群运营，使得用户可以方便快捷地取用数据。',
    install_requires = [
        "pandas>=0.23.4",
        "pyyaml>=5.3.1",
        "requests>=2.7.0"
    ],
    packages=find_packages(),
    data_file = "hs_udata\\utils\\config.yml",
    include_package_data = True,
    #包含所有.xlsx文件
    package_data = {
        '':['*.yml'],
    }


)