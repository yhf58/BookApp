from django.db import models

## 把模型映射到数据库中

# 1.python manage.py makemigrations   生成迁移脚本文件

# 2.使用migrate 将新生成的迁移脚本文件映射到数据中

class Person(models.Model):

    #主键自增长
    id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,null=False)
    age=models.IntegerField(max_length=10,null=False,default=1)


class Publisher(models.Model):
    name=models.CharField(max_length=100,null=False)
    address=models.CharField(max_length=100,null=False)

class book(models.Model):
    #主键自增长
    id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,null=False)
    author=models.CharField(max_length=100,null=False)
