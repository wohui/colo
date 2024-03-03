from django.db import models

# Create your models here.

class Plan(models.Model):
    """colo 测试计划表"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    script = models.TextField()
    user_count = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    owner = models.CharField(max_length=32,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
class TestRecord(models.Model):
    """colo 测试计划表"""
    id = models.AutoField(primary_key=True)
    pid = models.CharField(max_length=255)
    plan_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id