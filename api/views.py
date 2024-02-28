import json

from django.http import JsonResponse

from api.models import Plan, TestRecord
from util.cmd import CMD
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


def execute_plan_view(request):
    plan_info = json.loads(request.body)
    # 执行locust命令
    cmd_handle = CMD()
    pid = cmd_handle.run(
        'locust --timescale --headless --override-plan-name 228002 -f .\locust_case\locustfile.py --run-time 1m')
    print(f'pid--{pid}')
    # 生成测试执行记录，在测试执行记录页面查询和停止
    record_info = {
        'plan_name': plan_info['name'],
        'pid': pid
    }
    TestRecord.objects.create(**record_info)
    # check_res_list = Plan.objects.filter().values()
    res = {
        'code': 0
    }
    return JsonResponse(res, safe=False)


def get_test_record_view(request):
    query_res = TestRecord.objects.filter().values()
    res = {
        'data': {
            'total': len(query_res),
            'list': list(query_res)
        },
        'code': 0,
    }
    return JsonResponse(res, safe=False)


def stop_execute_plan_view(request):
    pid = json.loads(request.body)['pid']
    # 执行locust命令
    cmd_handle = CMD()
    cmd_handle.kill_process(int(pid))
    res = {
        'code': 0
    }
    return JsonResponse(res, safe=False)


def create_plan_view(request):
    """
    1.生成测试计划，保存任务信息到数据库
    2.可以编辑？
    3、
    """
    plan_info = json.loads(request.body)

    Plan.objects.create(**plan_info)
    # check_res_list = Plan.objects.filter().values()

    res = {
        'data': {

        },
        'code': 0,
    }
    return JsonResponse(res, safe=False)


def get_plan_view(request):
    query_res = Plan.objects.filter().values()
    res = {
        'data': {
            'total': len(query_res),
            'list': list(query_res)
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
