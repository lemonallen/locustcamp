import random, json
from locust import SequentialTaskSet, HttpUser, between, task, tag


class TaskSuit(SequentialTaskSet):
    # 类继承SequentialTaskSet 或 TaskSet类
    # 当类里面的任务请求有先后顺序时，继承SequentialTaskSet类，
    # 没有先后顺序，可以使用继承TaskSet类
    def on_start(self):
        self.headers = {"Content-Type": "application/json"}
        self.username = "locust_" + str(random.randint(10000, 100000))
        self.pwd = '1234567890'

    def on_stop(self):
        pass

    @task
    @tag("leave_1")
    def regist_case(self):  # 一个方法， 方法名称可以自己改
        url = '/erp/regist'  # 接口请求的URL地址
        # 定义请求头为类变量，这样其他任务也可以调用该变量

        # post请求的 请求体
        data = {"name": self.username, "pwd": self.pwd}
        # 使用self.client发起请求，请求的方法根据接口实际选,
        # catch_response 值为True 允许为失败 ，
        # name 设置任务标签名称   -----可选参数
        with self.client.post(url, data=json.dumps(data), headers=self.headers, catch_response=True,
                              name="case_1_register") as rsp:
            if rsp.status_code > 400:
                print(rsp.text)
                rsp.failure('regist_ 接口失败！')

    @task  # 装饰器，说明下面是一个任务
    def login_case(self):
        url = '/erp/loginIn'  # 接口请求的URL地址
        data = {"name": self.username, "pwd": self.pwd}
        with self.client.post(url, data=json.dumps(data), headers=self.headers, catch_response=True,
                              name="case_2_login") as rsp:
            # 提取响应json 中的信息，定义为 类变量
            self.token = rsp.json()['token']
            if rsp.status_code < 400 and rsp.json()['code'] == "200":
                rsp.success()
            else:
                rsp.failure('login登录失败！')

    @task  # 装饰器，说明下面是一个任务
    def getuser_case(self):
        url = '/erp/user'  # 接口请求的URL地址
        # 引用上一个任务的 类变量值   实现参数关联
        headers = {"Token": self.token}
        # 使用self.client发起请求，请求的方法 选择 get
        with self.client.get(url, headers=headers, catch_response=True, name="case_3_getuser") as rsp:
            if rsp.status_code < 400:
                rsp.success()
            else:
                rsp.failure('getuser获取用户信息失败！')


class TaskPlan(HttpUser):
    # task_set属性已经被移除， tasks属性值必须为列表或字典
    tasks = [TaskSuit]
    wait_time = between(0.01, 3)
