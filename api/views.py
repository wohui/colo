import json

from django.shortcuts import render
from django.http import JsonResponse

from util.file import LocustFile
# Create your views here.

def test_view(request):
    res= {
        'data':[1,2,3]
    }
def test_generate(request):
    api_url='http://www.baidu.com'
    res=[]
    return JsonResponse(res,safe=False)
def create_task_view(request):
    """
    1、获取到任务信息，生成locustfile
    2、将以上信息，生成一个未开始的任务，保存到平台数据库
    3、
    """
    task_info = {
        'name':'test_plan_1',
        'locust_data':[
            {
                "host": "http://192.168.0.101:8000",
                "path": "/get_data/test"
            },
            {
                "host": "http://192.168.0.101:8000",
                "path": "/say_hello/hui"
            },
            {
                "host": "http://192.168.0.101:8000",
                "path": "/t1"
            },
        ],

    }
    locust_flie = LocustFile()
    file_name = locust_flie.create(task_info['name'],task_info['locust_data'])
    if file_name != '':
        pass
    else:
        res = {
            'code':-1,
            'msg':'生成locustfile失败'
        }
    # 开始写信息到数据库

    res= {
        'res': 'OKK'
    }
    return JsonResponse(res,safe=False)
def run_task_view(request):
    api_url='http://www.baidu.com'
    res=[]
    return JsonResponse(res,safe=False)
