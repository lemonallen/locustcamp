
from locust import SequentialTaskSet, HttpUser, between, task, tag

class TaskSuit(SequentialTaskSet):
    # 类继承SequentialTaskSet 或 TaskSet类
    # 当类里面的任务请求有先后顺序时，继承SequentialTaskSet类，
    # 没有先后顺序，可以使用继承TaskSet类
    def on_start(self):
        pass

    def on_stop(self):
        pass

class TaskPlan(HttpUser):
    # task_set属性已经被移除， tasks属性值必须为列表或字典
    tasks = [TaskSuit]
    wait_time = between(0.01, 3)