from django.db import models


# Create your models here.

class TestMachine(models.Model):
    """测试机器表"""
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=255)
    hardware_info = models.CharField(max_length=255)
    owner = models.CharField(max_length=32)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
