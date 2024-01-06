# !/usr/local/bin/python
# -*- coding:utf-8 -*-
from locust import HttpUser, TaskSet, task, between,run_single_user
'''
测试demo脚本，请替换成自己的压测脚本
'''
from locust_plugins import listeners
from locust import HttpUser, task, events
# import os
# os.environ['PGHOST'] = '127.0.0.1'
# os.environ['PGUSER'] = 'postgres'
# os.environ['PGPASSWORD'] = 'hui666666'
# os.environ['PGDATABASE'] = 'postgres'
class NoSlowQTaskSet(HttpUser):
    host = "http://192.168.0.101:8000"
    @task(2)
    def get_data(self):
        r = self.client.get("/get_data/test")
    @task(8)
    def say_hello(self):
        r = self.client.get("/say_hello/hui")

    def on_locust_init(self,environment, **_kwargs):
        listeners.Timescale(env=environment, testplan="timescale_listener_ex")
if __name__ == "__main__":
    run_single_user(NoSlowQTaskSet)

