from django.db import models


# Create your models here.
class FavoriteList(models.Model):
    user = models.TextField(verbose_name='用戶')
    name = models.TextField(verbose_name='名稱')
    video_id = models.TextField(verbose_name='ID')
    created_at = models.DateTimeField(auto_now=True, verbose_name='創建日期')