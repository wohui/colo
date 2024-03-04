import subprocess
import time

import psutil
# 会写到文件中
from nb_log import get_logger

logger = get_logger('colo_log',
                    log_filename='colo.log',
                    error_log_filename='colo_error.log')


class CMD():
    def __init__(self):
        self.cmd_list = []

    def run(self, cmd):
        "执行cmd命令"
        logger.info(cmd)
        proc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f'id={proc.pid}')
        pid = proc.pid
        return pid

    def kill_process(self, pid):
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
    import os
    cmd = 'locust --timescale --headless --host http://192.168.0.101:8000 -u 2 -r 1 --override-plan-name 测试用户系统核心2个接口-1709542579262926900 -f "D:\py_space\colo\locust_case\locustfile_1.py" --pghost 192.168.0.101 --pgport 5432 --pguser postgres --pgpassword hui666666 --pgdatabase colo_test --run-time 3600s'
    import subprocess
    proc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid = proc.pid
    time.sleep(30)
    process = psutil.Process(pid)
    process.terminate()
