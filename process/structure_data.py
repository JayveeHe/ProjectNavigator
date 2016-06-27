# coding=utf-8
import hashlib
import re
import sys
import arrow
from utils.common_utils import timer
from utils.dao_utils.mongo_utils import get_db_inst

reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'jayvee'


@timer
def structure_data():
    db_sp = get_db_inst('ProjectNavi', 'ScenicPoins')
    find_result = db_sp.find()
    for item in find_result:
        title = item['title']
        city = item['city']
        addr = item['address']
        tmp = city + title + addr
        md5 = hashlib.md5(tmp).hexdigest()
        open_time = item['infos'].get('open_time', None)
        structured_open_time = analyze_open_time(open_time)
        visit_time = item['infos'].get('visit_time', None)
        structured_visit_time = analyze_visit_time(visit_time)
        print title
        print open_time, structured_open_time
        print visit_time, structured_visit_time
        structured_data = {'open_time': {"start": structured_open_time[0], 'end': structured_open_time[1]},
                           'visit_time': structured_visit_time}
        item['structured_infos'] = structured_data
        item['md5'] = md5
        try:
            db_sp.update({'title': title, 'city': city}, item)
        except Exception, e:
            print e


def analyze_open_time(str_open_time):
    if str_open_time:
        f_result = re.findall('\d{1,2}:\d{1,2}-\d{1,2}:\d{1,2}', str_open_time)
        if f_result:
            start = 0
            end = 2400
            for i in f_result:
                sp = i.split('-')
                tmp_start = int(sp[0].split(':')[0]) * 100
                tmp_start += int(sp[0].split(':')[1])
                start = max(start, tmp_start)
                tmp_end = int(sp[1].split(':')[0]) * 100
                tmp_end += int(sp[1].split(':')[1])
                end = min(end, tmp_end)
            return start, end
        f_result = re.findall('\d{1,2}:\d{1,2}~\d{1,2}:\d{1,2}', str_open_time)
        if f_result:
            start = 0
            end = 2400
            for i in f_result:
                sp = i.split('~')
                tmp_start = int(sp[0].split(':')[0]) * 100
                tmp_start += int(sp[0].split(':')[1])
                start = max(start, tmp_start)
                tmp_end = int(sp[1].split(':')[0]) * 100
                tmp_end += int(sp[1].split(':')[1])
                end = min(end, tmp_end)
            return start, end
        if re.findall(u'全天', str_open_time):
            return 600, 2300
        return 600, 2400
    else:
        return 600, 2400


def analyze_visit_time(str_visit_time):
    """
    分析参观时间文本，返回以分钟为单位的参观时间（int）
    :param str_visit_time:
    :return:
    """
    if str_visit_time:
        # 匹配分钟
        if re.findall(u'(\d{0,3}[-~]?\d{0,3})分钟', str_visit_time):
            f_result = re.findall(u'(\d{1,3}[-~]\d{1,3})分钟', str_visit_time)
            # 匹配到范围时间
            if f_result:
                split = re.split('[-~]', f_result[0])
                visit_minute = (int(split[0]) + int(split[1])) / 2
                return visit_minute
            # 匹配到具体时间
            f_result = re.findall(u'(\d{1,3})分钟', str_visit_time)
            if f_result:
                return int(f_result[0])
        # 匹配小时
        if re.findall(u'(\d{0,3}[-~]?\d{0,3})小时', str_visit_time):
            f_result = re.findall(u'(\d{1,3}[-~]\d{1,3})小时', str_visit_time)
            # 匹配到范围时间
            if f_result:
                split = re.split('[-~]', f_result[0])
                visit_hour = (int(split[0]) + int(split[1])) / 2.0
                return int(visit_hour * 60)
            # 匹配到具体时间
            f_result = re.findall(u'(\d{1,3})小时', str_visit_time)
            if f_result:
                return int(f_result[0]) * 60
        # 匹配天，简单地使用如下规则：出现“天”则默认餐馆6小时
        if re.findall(u'天', str_visit_time):
            return 6 * 60
    return 1 * 60  # 默认参观时间1小时


if __name__ == '__main__':
    structure_data()
