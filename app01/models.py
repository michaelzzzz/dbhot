from django.db import models


# Create your models here.
class Admin(models.Model):
    """管理员"""
    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)

class Deparament(models.Model):
    """部门表"""
    title = models.CharField(verbose_name='标题', max_length=32)

    # 这边为了输出定制的title，解决view.py里UserModelForm类输出对象的问题，可以去除下面两行试一试
    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """员工表"""
    # 类型是CharField的必须需要加max_length
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    # 最大长度是10，小数点后面2位，默认是0
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name='入职时间')
    create_time = models.DateField(verbose_name='入职时间')
    # 有约束
    #   to,与哪张表有关联
    #   to_field,表中的那一列关联
    #   目前定义的名字是depart，但是django生成的数据列名称为depart_id
    # 1.级联删除
    depart = models.ForeignKey(verbose_name='部门', to="Deparament", to_field='id', on_delete=models.CASCADE)
    # 2.可以置空
    # depart = models.ForeignKey(to="Deparament",to_field='id',null=True,blank=True,on_delete=models.SET_NULL)
    # 在django中做约束
    gender_choices = (
        (2, "男"),
        (1, "女"),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)


class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    price = models.IntegerField(verbose_name="价格", default=0)
    level_choice = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choice, default=1)
    status_choice = (
        (1, "已占用"),
        (2, "未占用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choice, default=2)
