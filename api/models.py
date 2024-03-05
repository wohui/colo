from django.db import models


# Create your models here.

class Plan(models.Model):
    """colo 测试计划表"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    script = models.TextField()
    user_count = models.IntegerField(default=1)
    spawn_rate = models.IntegerField(default=1)
    duration = models.IntegerField(default=1)
    owner = models.CharField(max_length=32, default=None)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class TestRecord(models.Model):
    """colo 测试计划表"""
    id = models.AutoField(primary_key=True)
    pid = models.CharField(max_length=255)
    plan_name = models.CharField(max_length=255)
    test_plan_id = models.CharField(max_length=255,default=None)
    status = models.IntegerField(default=0)
    monitor_url = models.CharField(max_length=255, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
