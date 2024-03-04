import json
import time

from django.http import JsonResponse
from nb_log import get_logger
from django.core.paginator import Paginator
from api.models import Plan, TestRecord
from util.cmd import CMD
from util.file import LocustFile

# 会写到文件中
logger = get_logger('colo_log',
                    log_filename='colo.log',
                    error_log_filename='colo_error.log')


# logger = get_logger('log',)

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
    try:
        msg = ''
        plan_info = json.loads(request.body)
        host = 'http://192.168.0.101:8000'
        user_count = plan_info['user_count']
        spawn_rate = plan_info['spawn_rate'] #--spawn-rate
        script = plan_info['script']
        duration = plan_info['duration']  # 单位 秒
        test_plan_name = f'{plan_info['name']}-{time.time_ns()}'
        script_path = f'.\locust_case\\{script}'
        locust_cmd = (f'locust --timescale --headless'
                      f' --host {host}'
                      f' -u {user_count}'
                      f' -r {spawn_rate}'
                      f' --override-plan-name {test_plan_name}'
                      f' -f {script_path}'
                      f' --pghost 192.168.0.101'
                      f' --pgport 5432'
                      f' --pguser postgres'
                      f' --pgpassword hui666666'
                      f' --pgdatabase colo_test'
                      f' --run-time {duration}s')
        # 执行locust命令
        cmd_handle = CMD()
        pid = cmd_handle.run(locust_cmd)

        logger.info(f'pid--{pid}')
        # 配置监控地址，根据生成的test_plan_name+提前配置好的grafana地址组成
        monitor_url = f'http://192.168.0.101:3000/d/xh6zZMASk/colo_101?orgId=1&var-testplan={test_plan_name}&from=now-5m&to=now'
        # 生成测试执行记录，在测试执行记录页面查询和停止
        record_info = {
            'plan_name': plan_info['name'],
            'pid': pid,
            'monitor_url': monitor_url
        }
        TestRecord.objects.create(**record_info)
    except Exception as e:
        logger.error(f'执行测试计划时发生错误-{e}')
        msg = f'发生错误-{e}'
    # check_res_list = Plan.objects.filter().values()
    res = {
        'code': 0,
        'msg': msg,
        'data': [1,2,3]
    }
    return JsonResponse(res, safe=False)


def get_all_script_view(request):
    # page_size = int(request.GET.get('size'))
    # page_number = int(request.GET.get('currentPage'))
    #
    # plan_query = Sc.objects.filter().values().order_by('-created_at')
    #
    # # 创建Paginator对象
    # paginator = Paginator(plan_query, page_size)
    #
    # # 获取指定页数的数据
    # page_obj = paginator.get_page(page_number)
    # # 获取当前页的数据列表
    # data_list = page_obj.object_list
    res = {
        'data': {
            'total': 6,
            'list': [
                {
                    'name': '获取订单详情接口',
                    'user': '库萨克'
                },
                {
                    'name': '设置会员信息接口',
                    'user': '滴滴答答'
                }
            ]
        },
        'code': 0,
    }
    return JsonResponse(res, safe=False)


def get_test_record_view(request):
    page_size = int(request.GET.get('size'))
    page_number = int(request.GET.get('currentPage'))

    test_record_query = TestRecord.objects.filter().values().order_by('-created_at')

    # 创建Paginator对象
    paginator = Paginator(test_record_query, page_size)

    # 获取指定页数的数据
    page_obj = paginator.get_page(page_number)
    # 获取当前页的数据列表
    data_list = page_obj.object_list

    res = {
        'data': {
            'total': len(test_record_query),
            'list': list(data_list)
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


def update_plan_view(request):
    """
    1.生成测试计划，保存任务信息到数据库
    2.可以编辑？
    3、
    """
    plan_info = json.loads(request.body)
    plan_id = plan_info['id']
    Plan.objects.filter(id=plan_id).update(**plan_info)
    # check_res_list = Plan.objects.filter().values()

    res = {
        'data': {

        },
        'code': 0,
    }
    return JsonResponse(res, safe=False)


def get_plan_view(request):
    page_size = int(request.GET.get('size'))
    page_number = int(request.GET.get('currentPage'))

    plan_query = Plan.objects.filter().values().order_by('-created_at')

    # 创建Paginator对象
    paginator = Paginator(plan_query, page_size)

    # 获取指定页数的数据
    page_obj = paginator.get_page(page_number)
    # 获取当前页的数据列表
    data_list = page_obj.object_list
    res = {
        'data': {
            'total': len(plan_query),
            'list': list(data_list)
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
