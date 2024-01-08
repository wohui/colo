from django.shortcuts import render
from django.http import JsonResponse

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
    1、获取到任务信息，生成timescaledb数据库，生成locustfile
    2、将以上信息，生成一个未开始的任务，保存到平台数据库
    3、
    """
    task_info = []
    # 创建数据库

    res=[]
    return JsonResponse(res,safe=False)
def run_task_view(request):
    api_url='http://www.baidu.com'
    res=[]
    return JsonResponse(res,safe=False)
