# coding:utf-8
"""
* 作者：王若宇
* 时间：2022/1/25 14:00
* 功能：打包Python软件包用于发布到pypi.org
* 说明：请看读我.txt，库发布后可使用学而思库管理工具下载
"""
import sys

from setuptools import setup
from xes import AIspeak

if __name__ == '__main__':
    sys.argv += ["sdist"]
setup(
    name='PySet2',
    version='0.0.1',
    packages=['PySet2'],
    url='https://yangguang-gongzuoshi.top/wry/',
    license='MIT License',
    author='Ruoyu Wang',
    author_email='wry2022@outlook.com',
    description='PySide2设置工具/' + AIspeak.translate('PySide2设置工具'),
    long_description='简易地设置和转换PySide2文件，并可以储存字段。。/' + AIspeak.translate('简易地设置和转换PySide2文件，并可以储存字段。。'),
    requires=["PyQt5"]
)
