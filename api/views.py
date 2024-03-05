import json
import os
import time

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.paginator import Paginator
from django.http import JsonResponse
from nb_log import get_logger

from api.models import Plan, TestRecord
from util.cmd import CMD
from util.file import LocustFile

# 会写到文件中
logger = get_logger('colo_log',
                    log_filename='colo.log',
                    error_log_filename='colo_error.log')


# logger = get_logger('log',)

# Create your views here.
def start_locust_view(request):
    test_plan_name = request.GET.get('test_plan_name')
    logger.info(f'测试开始-{test_plan_name}')
    return JsonResponse({}, safe=False)


def stop_locust_view(request):
    test_plan_name = request.GET.get('test_plan_name')
    logger.info(f'测试已结束-{test_plan_name}')
    TestRecord.objects.filter(test_plan_id=test_plan_name).update(status=2)
    return JsonResponse({}, safe=False)


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
    msg = ''
    code = 0
    try:

        plan_info = json.loads(request.body)
        host = 'http://192.168.0.101:8000'
        user_count = plan_info['user_count']
        spawn_rate = plan_info['spawn_rate']  # --spawn-rate
        script_name = plan_info['script']
        duration = plan_info['duration']  # 单位 秒
        test_plan_id = f'{plan_info['name']}-{str(time.time_ns())[:2]}'
        owner = plan_info['owner']
        # 获取当前文件绝对路径的的上2层目录
        parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 获取脚本的绝对路径
        locust_file_path = os.path.join(parent_directory, "locust_case", f'{script_name}')
        logger.info(f'脚本路径{locust_file_path}')
        # script_path = f'.\locust_case\\{script}'
        locust_cmd = (f'locust --timescale --headless'
                      f' --host {host}'
                      f' -u {user_count}'
                      f' -r {spawn_rate}'
                      f' --override-plan-name {test_plan_id}'
                      f' -f {locust_file_path}'
                      f' --pghost 192.168.0.101'
                      f' --pgport 5432'
                      f' --pguser postgres'
                      f' --pgpassword hui666666'
                      f' --pgdatabase colo_test'
                      f' --run-time {duration}s')
        # 执行locust命令
        cmd_handle = CMD()
        pid, status = cmd_handle.run(locust_cmd)
        # 说明出现异常了，运行未成功
        if pid == -1 or status != 1:
            msg = '运行命令发生错误，请排查'
            code = -1
        else:
            # 配置监控地址，根据生成的test_plan_name+提前配置好的grafana地址组成
            monitor_url = f'http://192.168.0.101:3000/d/xh6zZMASk/colo_101?orgId=1&var-testplan={test_plan_id}&from=now-5m&to=now'
            # 生成测试执行记录，在测试执行记录页面查询和停止
            record_info = {
                'test_plan_id': test_plan_id,
                'plan_name': plan_info['name'],
                'pid': pid,
                'status': status,
                'owner': owner,
                'monitor_url': monitor_url
            }
            TestRecord.objects.create(**record_info)
            # 启动一个定时任务，开始时间为当前时间+duration，没10秒查询下pid状态
            scheduler = BackgroundScheduler()
    except Exception as e:
        logger.error(f'执行测试计划时发生异常-{e}')
        msg = f'execute_plan_view捕捉到异常-{e}'
    res = {
        'code': code,
        'msg': msg,
        'data': [1, 2, 3]
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
    status = cmd_handle.kill_process(int(pid))
    msg = ''
    if status == 2:
        TestRecord.objects.filter(pid=pid).update(status=2)
        msg = '终止测试正常'
    if status == 99:
        TestRecord.objects.filter(pid=pid).update(status=99)
        msg = '终止测试异常'
    res = {
        'code': 0,
        'msg': msg
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
