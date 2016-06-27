# coding=utf-8
import random
import time
from crawlers.mafengwo import query_by_name, get_details
from utils.common_utils import timer
from utils.dao_utils.mongo_utils import get_db_inst
from utils.log_utils import api_logger

__author__ = 'jayvee'


@timer
def get_city_scenic_points(city_name):
    """
    从mafengwo爬取指定城市的所有景点信息并存入数据库
    :param city_name:
    :return:
    """
    db_sp = get_db_inst('ProjectNavi', 'ScenicPoins')
    for info in query_by_name(city_name):
        print info['name']
        url = info['url']
        print url
        try:
            scenic_info = get_details(url)
            scenic_info['city'] = city_name
            db_sp.insert(scenic_info)
            api_logger.info('%s %s inserted' % (city_name, scenic_info['title']))
        except Exception, e:
            print e
        t = random.random() * 2
        print 'sleep %s seconds' % t
        time.sleep(t)


if __name__ == '__main__':
    get_city_scenic_points(u'北京')
