# -*- coding: utf-8 -*-

from configparser import ConfigParser

config = ConfigParser()
config.read(filenames='config/config.ini')


class ServerConfig():
    def __init__(self):
        section = 'Server'
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
