import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from nb_log import get_logger

from api.models import SysConfig

# 会写到文件中
logger = get_logger('colo_log',
                    log_filename='colo.log',
                    error_log_filename='colo_error.log')


# logger = get_logger('log',)

# Create your views here.
def create_config_view(request):
    msg = ''
    req_info = json.loads(request.body)
    try:
        config = SysConfig(name=req_info['name'],
                           content=json.loads(req_info['content']),
                           status=0)
        config.save()
        # SysConfig.objects.create(**req_info)
    except Exception as e:
        logger.error(f'create_config_view发生异常-{e}')
        msg = e
    res = {
        'code': 0,
        'msg': msg,
        'data': {}
    }
    return JsonResponse(res, safe=False)


def delete_config_view(request):
    body = json.loads(request.body)
    SysConfig.objects.get(id=body['id']).delete()
    res = {
        'code': 0,
        'msg': 'ok'
    }
    return JsonResponse(res, safe=False)


def update_config_view(request):
    req_info = json.loads(request.body)
    config_id = req_info['id']
    config = SysConfig.objects.get(id=config_id)
    config.name = req_info['name']
    config.content = json.loads(req_info['content'])
    config.save()
    res = {
        'code': 0,
        'msg': 'ok'
    }
    return JsonResponse(res, safe=False)


def get_config_view(request):
    page_size = int(request.GET.get('size'))
    page_number = int(request.GET.get('currentPage'))
    query_res = SysConfig.objects.filter().values().order_by('-created_at')
    # 创建Paginator对象
    paginator = Paginator(query_res, page_size)
    # 获取指定页数的数据
    page_obj = paginator.get_page(page_number)
    # 获取当前页的数据列表
    data_list = page_obj.object_list
    res = {
        'data': {
            'total': len(query_res),
            'list': list(data_list)
        },
        'code': 0,
    }
    return JsonResponse(res, safe=False)
