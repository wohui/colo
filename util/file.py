import os.path
import time,datetime

class LocustFile():
    def __init__(self):
        pass

    def create(self,locust_data):
      """Creates a Python file containing the given functions.

      Args:
        function_names: A list of strings containing the names of the functions.
        function_outputs: A list of strings containing the outputs of the functions.

      Returns:
        A string containing the contents of the Python file.
      """

      file_contents = ""
      file_contents += f"# !/usr/local/bin/python\n"
      file_contents += f"# -*- coding:utf-8 -*-\n"
      file_contents += f"from locust import HttpUser, TaskSet, task, between,run_single_user\n"
      file_contents += f"class NoSlowQTaskSet(HttpUser):\n"
      for index,item in enumerate(locust_data):
        file_contents += f"   host = \"http://192.168.0.101:8000\"\n"
        file_contents += f"   @task(5)\n"
        file_contents += f"   def locust_method_{index+1}(self):\n"
        file_contents += f"       r = self.client.get(\"{item['path']}\")\n"

      now_time = datetime.datetime.now()
      format_time = now_time.strftime("%Y_%m_%d_%H_%M_%S_%f")
      file_name = f"locust_case/colo_{format_time}@locustfile.py"
      with open(file_name, mode="w") as f:
        f.write(file_contents)
      return f'colo_{format_time}@locustfile.py'

if __name__ == "__main__":
  locust_data = [
    {
      "host": "http://192.168.0.101:8000",
      "path": "/get_data/test"
    },
    {
      "host": "http://192.168.0.101:8000",
      "path": "/say_hello/hui"
    },
  ]
  locust_flie = LocustFile()
  file_contents = locust_flie.create(locust_data)
  now_time = datetime.datetime.now()
  format_time = now_time.strftime("%Y_%m_%d_%H_%M_%S_%f")
# 打印结果
  print(format_time)
  with open(f"colo_{format_time}@locustfile.py", "w") as f:
    f.write(file_contents)
  print("File created successfully!")