from django.db import models

# Create your models here.

class Exceptions(models.Model):
    """locust 异常表"""
    id = models.AutoField(primary_key=True)
    Count = models.IntegerField(max_length=255)
    Message = models.TextField()
    Nodes = models.TextField()
    Traceback = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title