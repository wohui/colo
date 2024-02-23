import json

from django.http import JsonResponse

from util.file import LocustFile


# Create your views here.

def test_view(request):
    res = {
        'data': {
            'username': 'admin',
            'token': 'admin-token',
        },
        'code': 0,
        'message': '登录成功'
    }
    return JsonResponse(res, safe=False)


def users_info_view(request):
    res = {"code": 0, "data": {"username": "admin", "roles": ["admin"]}, "message": "获取用户详情成功"}
    return JsonResponse(res, safe=False)


def test_generate(request):
    api_url = 'http://www.baidu.com'
    res = []
    return JsonResponse(res, safe=False)


def get_plan_view(request):
    res = {
        'data': {
            'total': 24,
            'list': [{
                'name': "用户压测",
                "url": "http://192.68.1.101:8888",
                'ratio': 11
            },
                {
                    'name': "登录试试",
                    "url": "http://192.68.10.201:6666",
                    'ratio': 22
                }]
        },
        'code': 0,
    }
    return JsonResponse(res, safe=False)


def create_plan_view(request):
    """
    1.生成测试计划，保存任务信息到数据库
    2.可以编辑？
    3、
    """
    plan_info = json.loads(request.body)
    task_info = {
        'name': 'test_plan_1',
        'locust_data': [
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

    res = {
        'data': {
            'total': 24,
            'list': [{
                'name': "1",
                "url": "baidu",
                'ratio': 11
            },
                {
                    'name': "2",
                    "url": "baidu",
                    'ratio': 22
                }]
        },
        'code': 0,
    }
    return JsonResponse(res, safe=False)


def run_task_view(request):
    task_id = 1
    """
    1.根据taskid查询任务信息
    2.生成locustfile，开始执行，修改状态
    """
    locust_flie = LocustFile()
    file_name = locust_flie.create(task_id)
    if file_name != '':
        pass
    else:
        res = {
            'code': -1,
            'msg': '生成locustfile失败'
        }
    # 开始写信息到数据库

    api_url = 'http://www.baidu.com'
    res = []
    return JsonResponse(res, safe=False)
