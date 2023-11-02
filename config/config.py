# -*- coding: utf-8 -*-

from configparser import ConfigParser
import os
import sys

config = ConfigParser()

config.read(filenames='config/config.ini')

# path = os.getcwd()
# config.read(filenames='C:/work/stable-diffusion/config/config.ini')

# config_path = 'config/config.ini'
# print("Trying to load config from:", os.path.abspath(config_path))
# config.read(filenames=config_path)


class ServerConfig():
    def __init__(self):
        section = 'SERVER'
        self.host = config.get(section=section, option='host')
        self.port = config.getint(section=section, option='port')
        self.debug = config.getboolean(section=section, option='debug')


class DBConfig():
    def __init__(self):
        section = 'DB'
        self.mysql_host = config.get(section=section, option='mysql_host')
        self.mysql_port = config.getint(section=section, option='mysql_port')
        self.mysql_user = config.get(section=section, option='mysql_user')
        self.mysql_pwd = config.get(section=section, option='mysql_pwd')
        self.mysql_db = config.get(section=section, option='mysql_db')
        self.mysql_table = config.get(section=section, option='mysql_table')