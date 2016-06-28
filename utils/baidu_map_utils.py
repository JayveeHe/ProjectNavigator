# coding=utf-8
import json
import os
import random
import requests

__author__ = 'jayvee'

cur_path = os.path.dirname(__file__)
config = json.loads(open('%s/config.conf' % (cur_path), 'r').read())


def baidu_geocoder(addr_name):
    """
    根据地址文本获取gps坐标
    :param addr_name:
    :return:
    """
    ak = random.choice(config['baidu_ak'])
    url = 'http://api.map.baidu.com/geocoder/v2/'
    params = {'ak': ak, 'address': addr_name, 'output': 'json'}
    res = requests.get(url, params=params)
    # print res.text
    geo_res = json.loads(res.text)
    geo_res['type'] = 'baidu_map'
    return geo_res


def get_route_matrix(point_list):
    """
    获取多个起点到多个终点之间的距离和时间，最多为5X5
    :param point_list:
    :return:
    """
    ak = random.choice(config['baidu_ak'])
    url = 'http://api.map.baidu.com/direction/v1/routematrix'
    start_list = []
    for i in point_list:
        start_list.append('%s,%s' % (i.location['gps']['lat'], i.location['gps']['lng']))
    places_str = '|'.join(start_list)
    params = {'origins': places_str, 'destinations': places_str, 'ak': ak, 'output': 'json'}
    res = requests.get(url, params=params).text
    json_res = json.loads(res)
    req_result = json_res['result']['elements']
    item_count = len(point_list)
    mat = {}
    for x in xrange(item_count):
        item = point_list[x]
        targets = {}
        for j in xrange(item_count):
            target_item = point_list[j]
            target = req_result[x * item_count + j]
            targets[target_item.md5] = {'item': target_item, 'duration': target['duration']['value']}
        mat[item.md5] = {'item': item, 'targets': targets}
    return mat


def get_direction(origin, destination):
    """
    获取两点之间的路线信息
    :param origin:
    :param destination:
    :return:
    """
    pass


if __name__ == '__main__':
    pl = [{
        "location": {
            "type": "baidu_map",
            "gps": {
                "lat": 39.989669414786135349,
                "lng": 116.47061534841832042
            }
        }},
        {"location": {
            "type": "baidu_map",
            "gps": {
                "lat": 39.915445784824584052,
                "lng": 116.56270898880943321
            }
        }},
        {"location": {
            "type": "baidu_map",
            "gps": {
                "lat": 39.916672698100704508,
                "lng": 116.40377163503065105
            }
        }}]
    get_route_matrix(pl)
