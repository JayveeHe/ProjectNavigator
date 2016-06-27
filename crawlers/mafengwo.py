# encoding:utf8
import json
import os
import random
import re

import requests
from bs4 import BeautifulSoup
from utils.baidu_map_utils import baidu_geocoder

from utils.log_utils import api_logger

__author__ = 'jayvee'

cur_path = os.path.dirname(__file__)




def query_by_name(city_name):
    """
    根据城市名称获取相应的景点信息
    :param city_name:
    :return:
    """
    api_logger.info('start crawling %s' % city_name)
    q_url = 'http://www.mafengwo.cn/group/s.php'
    q_html = requests.get(q_url, {'q': city_name}).text
    q_soup = BeautifulSoup(q_html)
    scenic_url = q_soup.select('div.ser-title a')[0].attrs['href']
    scenic_id = re.findall('\d+', scenic_url)[0]
    city_url = 'http://www.mafengwo.cn/jd/%s/gonglve.html' % scenic_id
    api_logger.info('city url: %s' % city_url)
    scenic_point_list = get_scenic_points_list(city_url)
    for i in scenic_point_list:
        yield i


def get_scenic_points_list(url):
    """
    获取一个城市的所有景点及url
    :param url:城市页url
    :return:
    """
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    l = soup.select('div.list ul.clearfix li')
    res = []
    api_logger.info('%s has %s scenic points' % (url, len(l)))
    for i in l:
        a = i.select('a')[0]
        point_name = i.text.strip()
        point_url = 'http://www.mafengwo.cn%s' % a.attrs['href']
        yield {'name': point_name, 'url': point_url}
        # res.append({'name': point_name, 'url': point_url})
        # return res


def get_details(url):
    """
    获取一个景点的详情信息
    :param url: 景点url
    :return:
    """
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    scenic_point = soup.select('div.s-title h1')[0].text
    addr_title = soup.select('div.r-title div')[0].text.split(u'，')[0]
    intro_soup = soup.select('dl.intro dt span')
    if intro_soup:
        intro = intro_soup[0].text
    else:
        intro = ''
    other_infos = soup.select('dl.intro dd')
    infos = {}
    label_key_mapper = {u'电话': 'tel', u'交通': 'transport', u'门票': 'ticket',
                        u'开放时间': 'open_time', u'用时参考': 'visit_time', u'网址': 'website',
                        u'其他联系方式': 'other_contact'}
    if other_infos:
        for dd in other_infos:
            label = dd.select('span.label')[0].text.strip()
            info = dd.select('p')[0].text
            infos[label_key_mapper[label]] = info
    geo_details = baidu_geocoder(addr_title)
    scenic_info = {}
    scenic_info['title'] = scenic_point
    scenic_info['location'] = {'type': geo_details['type'], 'gps': geo_details['result']['location']}
    scenic_info['address'] = addr_title
    scenic_info['intro'] = intro
    scenic_info['infos'] = infos
    return scenic_info




if __name__ == '__main__':
    query_by_name('北京')
    # baidu_geocoder('故宫')
    # get_details('http://www.mafengwo.cn/poi/3474.html')
    # result = get_viewpoint_list('http://www.mafengwo.cn/jd/10065/gonglve.html')
    # with open('pois.json', 'w') as fout:
    #     fout.write(json.dumps(result))
