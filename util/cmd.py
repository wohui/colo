import logging
import subprocess
import time
import psutil
import subprocess
import os
import signal
import logging
# 会写到文件中
from nb_log import get_logger
logger = get_logger('colo_log',
                    log_filename='colo.log',
                    error_log_filename='colo_error.log')

class CMD():
    def __init__(self):
        self.cmd_list = []

    def run(self,cmd):
        "执行cmd命令"
        proc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f'id={proc.pid}')
        pid = proc.pid
        return pid
    def kill_process(self,pid):
        try:
            # 根据进程ID获取进程对象
            process = psutil.Process(pid)
            process_status = process.status()
            # os.kill(pid, signal.SIGTERM)
            process.terminate()
            logger.info(f"进程id-{pid}已经停止")
        except psutil.NoSuchProcess:
            logger.error(f"kill_process发生错误，指定的进程ID-{pid}-不存在")

        # 给 locust 进程发送终止信号

if __name__ == '__main__':
    from nb_log import get_logger

    # 会写到文件中
    logger = get_logger('colo_log',
                        log_filename='colo.log',
                        error_log_filename='colo_error.log')
    # logger = get_logger('log',)
    logger.info(1233)
    import sys
    print('试试')
    print(sys.path)
    print(sys.path[1])
        # cmd_handle = CMD()
        # cmd_handle.kill_process(19240)
        # id = cmd_handle.run('locust -f  ../locust_case/locustfile_2.py  --timescale --headless --override-plan-name 2331')
        # print(id)
        # import subprocess
        # import os
        # import signal
        #
        # locust_process = None
        #
        # def start_locust():
        #     global locust_process
        #
        #     # 检查是否已经有进程在运行
        #     if locust_process and locust_process.poll() is None:
        #         print('Locust 已经在运行')
        #     else:
        #         # 启动 locust 进程
        #         locust_process = subprocess.Popen('locust -f  ../locust_case/locustfile_2.py  --timescale --headless --override-plan-name 23322', shell=False)
        #         print(f'id={locust_process.pid}')
        #         print('Locust 已启动')
        #
        #
        # def stop_locust():
        #     global locust_process
        #
        #     # 检查是否有进程在运行
        #     if locust_process and locust_process.poll() is None:
        #         # 给 locust 进程发送终止信号
        #         os.kill(locust_process.pid, signal.SIGTERM)
        #         locust_process.wait()
        #         print('Locust 已停止')
        #     else:
        #         print('Locust 没有在运行')
