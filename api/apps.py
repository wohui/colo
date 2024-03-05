from django.apps import AppConfig
import os

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'


    # 可以保证不使用--noreload，init_method不会运行2次
    def ready(self):
        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE')
        if run_once is not None:
            return
        os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True'
        self.init_method()

    def init_method(self):
        # 在这里执行你想要在 Django 启动时执行的方法
        print("Django app is ready! Performing initialization...")
        # 添加你的自定义初始化逻辑