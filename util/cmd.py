import subprocess
class CMD():
    def __init__(self):
        self.cmd_list = []

    def run(self,cmd):
        "执行cmd命令"
        print(cmd)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        return stdout.decode('utf-8'), stderr.decode('utf-8')

if __name__ == '__main__':

        cmd_handle = CMD()
        stdout, stderr = cmd_handle.run('locust -f  ../locust_case/locustfile.py --headless -u 2 -r 1 -t 10s --csv=./')
        print(stdout)
        print(stderr)