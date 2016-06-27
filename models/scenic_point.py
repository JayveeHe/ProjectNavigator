# coding=utf-8
__author__ = 'jayvee'


class ScenicPoint(object):
    def __init__(self, info):
        self.gps = info['location']['gps']
        self.title = info['title']
        self.sid = info


def gen_seq(point_list, start_point):
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
    pl = [1, 2, 3]
    res1 = gen_seq(pl, 4)
    print res1
