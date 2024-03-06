import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from nb_log import get_logger

from env.models import TestMachine

# 会写到文件中
logger = get_logger('colo_log',
                    log_filename='colo.log',
                    error_log_filename='colo_error.log')


# logger = get_logger('log',)

# Create your views here.
def create_test_machine_view(request):
    test_machine_info = json.loads(request.body)
    TestMachine.objects.create(**test_machine_info)
    res = {
        'code': 0,
        'msg': 'ok',
        'data': {}
    }
    return JsonResponse(res, safe=False)


def delete_test_machine_view(request):
    body = json.loads(request.body)
    machine_id = body['id']
    TestMachine.objects.get(id=machine_id).delete()
    res = {
        'code': 0,
        'msg': 'ok'
    }
    return JsonResponse(res, safe=False)


def update_test_machine_view(request):
    plan_info = json.loads(request.body)
    plan_id = plan_info['id']
    TestMachine.objects.filter(id=plan_id).update(**plan_info)
    res = {
        'code': 0,
        'msg': 'ok'
    }
    return JsonResponse(res, safe=False)


def apply_test_machine_view(request):
    body = json.loads(request.body)
    machine_id = body['id']
    TestMachine.objects.filter(id=machine_id).update(status=1)
    res = {
        'code': 0,
        'msg': 'ok'
    }
    return JsonResponse(res, safe=False)


def get_test_machine_view(request):
    page_size = int(request.GET.get('size'))
    page_number = int(request.GET.get('currentPage'))
    test_machine_res = TestMachine.objects.filter().values().order_by('-created_at')
    # 创建Paginator对象
    paginator = Paginator(test_machine_res, page_size)

    # 获取指定页数的数据
    page_obj = paginator.get_page(page_number)
    # 获取当前页的数据列表
    data_list = page_obj.object_list
    res = {
        'data': {
            'total': len(test_machine_res),
            'list': list(data_list)
        },
        'code': 0,
    }
    return JsonResponse(res, safe=False)
