# !/usr/local/bin/python
# -*- coding:utf-8 -*-
from locust import HttpUser, TaskSet, task, between,run_single_user
'''
测试demo脚本，请替换成自己的压测脚本
'''
class NoSlowQTaskSet(HttpUser):
    host = "http://192.168.0.101:8000"
    @task(2)
    def get_data(self):
        r = self.client.get("/get_data/test")

    @task(8)
    def say_hello(self):
        r = self.client.get("/say_hello/hui")
if __name__ == "__main__":
    run_single_user(NoSlowQTaskSet)