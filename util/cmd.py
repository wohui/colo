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
        self.status = 0

    def run(self, cmd):
        pid = -1
        self.status = 0  # 未开始 0
        try:
            "执行cmd命令"
            logger.info(f'cmd run 收到的指令是-{cmd}')
            proc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pid = proc.pid
            # 等待5秒，查看状态
            time.sleep(3)
            process = psutil.Process(pid)
            process_status = process.status()
            logger.info(f'cmd 执行后查询到{pid}的状态')
            if process_status == 'running':
                self.status = 1  # 启动后=1
        except Exception as e:
            logger.error(f'MD run后 查询进程状态发生错误+{e}')
            self.status = 99  # 发生异常，查询不到进程，为99
        return pid, self.status

    def kill_process(self, pid):
        self.status = 1  # 默认kill掉之前的状态是运行 1
        try:
            # 根据进程ID获取进程对象
            process = psutil.Process(pid)
            process_status = process.status()
            process.terminate()
            logger.info(f"进程id-{pid}已经停止")
            self.status = 2  # 已停止
        except psutil.NoSuchProcess:
            logger.error(f"kill_process发生错误，指定的进程ID-{pid}-不存在")
            self.status = 99  # 异常
        return self.status
        # 给 locust 进程发送终止信号


if __name__ == '__main__':
    from nb_log import get_logger

    cmd = ('locust --timescale --headless --host http://192.168.0.101:8000 -u 2 -r 1 '
           '--override-plan-name 测试用户系统核心2个接口-140 -f D:\\py_space\\colo\\locust_case\\locustfile_1.py '
           '--pghost 192.168.0.101 --pgport 5432 --pguser postgres --pgpassword hui666666 --pgdatabase colo_test '
           '--run-time 3600s')
    ch = CMD()
    pid, status = ch.run(cmd)
    print(pid)
    print(status)
    status = ch.kill_process(pid)
    print(status)
