# coding=utf-8
__author__ = 'jayvee'


class ScenicPoint(object):
    def __init__(self, info):
        self.location = info['location']
        self.title = info['title']
        self.md5 = info['md5']
        self.city = info['city']
        self.address = info['address']
        self.infos = info['infos']
        self.visit_time = info['structured_infos']['visit_time']
        self.open_time = info['structured_infos']['open_time']
