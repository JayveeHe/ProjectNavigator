__author__ = 'jayvee'


class TourPlan(object):
    def __init__(self, start_time, plans=None):
        self.plan = []
        if plans:
            self.plan = plans
        self.start_time = start_time  # datetime

    def add_scenic_point(self, sp):
        self.plan.append(sp)

    def remove_scenic_point(self, sp):
        self.plan.remove(sp)

    def get_scenic_points(self):
        return self.plan
