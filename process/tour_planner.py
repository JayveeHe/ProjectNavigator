# coding=utf-8
from arrow import Arrow
from models.scenic_point import ScenicPoint
from models.tour_plan import TourPlan
from utils.baidu_map_utils import get_route_matrix
from utils.dao_utils.mongo_utils import get_db_inst

__author__ = 'jayvee'


def route_planner(point_list, start_point, start_time=None):
    """
    根据选出的景点进行计划规划，本模块的核心函数
    :param point_list: ScenicPoint类型的数组
    :param start_point: ScenicPoint类型的实例
    :return: TourPlan类型实例数组
    """
    if not start_time:
        start_time = Arrow.utcnow()
    pls = _gen_seq(point_list, start_point)
    route_mat = get_route_matrix(pls[0][:-1])
    for p_seq in pls:
        plan = TourPlan(start_time, p_seq)
        cost = _calc_plan_cost(plan, route_mat)


def _create_scenic_point_by_title(title):
    """
    根据title生成ScenicPoint对象实例
    :param title:
    :return:
    """
    db_sp = get_db_inst('ProjectNavi', 'ScenicPoins')
    find_result = db_sp.find_one({'title': title})
    sp = ScenicPoint(find_result)
    return sp


def _calc_plan_cost(plan, route_matrix):
    """
    计算某个计划的损失值
    :param plan:
    :param route_matrix:
    :return:
    """
    cur_time = plan.start_time
    sps = plan.get_scenic_points()
    last = sps[0]
    cost = 0
    for sp in sps[1:-1]:
        duration = route_matrix[last.md5][sp.md5]['duration']
        cur_time = cur_time.replace(minute=+duration)
        cur_hour = cur_time.hour() # todo 转换ScenicPoint中的时间范围变成datetime


def _gen_seq(point_list, start_point):
    """
    枚举所有可能的顺序序列
    :param point_list: 形如[ScenicPoint]的数组
    :param start_point:
    :return:
    """
    # plist = []
    # plist.remove()
    def dfs(plist):
        """
        生成全排列
        :param plist:
        :return:
        """
        if len(plist) > 0:
            res = []
            if len(plist) > 1:
                for i in xrange(len(plist)):
                    # tmp.append(plist[i])
                    t = plist[i]
                    # tt = plist[0]
                    plist[i] = plist[0]
                    plist[0] = t
                    r = dfs(plist[1:])
                    tmp = [t]
                    for j in r:
                        tmp.extend(j)
                        res.append(tmp)
                        tmp = [t]
                        # tmp = tmp[:-1]
                return res
            else:
                return [[plist[0]]]
        else:
            return []

    a_seq = dfs(point_list)
    result = []
    for seq in a_seq:
        result.append([start_point] + seq + [start_point])
    return result


if __name__ == '__main__':
    # s1 = _create_scenic_point_by_title('北京大学')
    # s2 = _create_scenic_point_by_title('颐和园')
    # s3 = _create_scenic_point_by_title('玉渊潭公园')
    # home = _create_scenic_point_by_title('天安门广场')
    # pls = _gen_seq([s1, s2, s3], home)
    # plan = TourPlan(Arrow.utcnow(), pls[0])
    # _calc_plan_cost(plan)
    pass
