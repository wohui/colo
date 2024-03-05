
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from nb_log import get_logger
from util.cmd import CMD

from api.models import TestRecord
logger = get_logger('colo_log',
                    log_filename='colo.log',
                    error_log_filename='colo_error.log')

class TestTask(object):
    _instance_lock = threading.Lock()

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(TestTask, "_instance"):
            with TestTask._instance_lock:
                TestTask._instance = TestTask(*args, **kwargs)
        return TestTask._instance

    def __init__(self):
        self._scheduler = BackgroundScheduler()

    def query_status(self):
        logger.info(f'新一轮定时任务查询测试计划执行状态开始')
        # 查询正在测试中的任务
        lock = threading.Lock()
        cmd_handle = CMD()
        with lock:
            query_res = TestRecord.objects.filter(status=1).values()
            if len(query_res) == 0:
                pass
            else:
                for item in query_res:
                    pid = int(item['pid'])
                    process_staus = cmd_handle.query_status_by_pid(pid)
                    if process_staus == 1:  # 测试中，不做处理
                        pass
                    else: # 如果查不到，说明测试完成了，有个问题，如果有个进程刚创建状态=1，然后被定时任务查询到的时候，找不到进程的话，会被认为完成
                        TestRecord.objects.filter(pid=pid).update(status=2)

    def set_status(self):
        pass

    def start_scheduler(self):
        logger.info('定时任务开启，start_scheduler')
        self._scheduler.add_job(self.query_status, 'interval', seconds=10, id='query_status')
        self._scheduler.start()
