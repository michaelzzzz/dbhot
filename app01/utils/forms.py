
from app01 import models
from django import forms
from app01.utils.bootstrapform import bootstrapform
from django.core.exceptions import ValidationError


class UserModelForm(bootstrapform):
    name = forms.CharField(min_length=3, label="用户名")

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'create_time', 'account', 'gender', 'depart']
        # widgets={
        #     "name":forms.TextInput(attrs={"class":"form-control"}),
        #     "password":forms.PasswordInput(attrs={"class":"form-control"})
        # }

class PrettyModelForm(bootstrapform):
    # 验证方式1
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}', '手机号格式错误')],
    # )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

        # fields = "__all__"
        # 排除某个字段
        # exclude = ['level']

    # 验证方式2
    # clean_字段名，钩子方法
    def clean_mobile(self):
        # 钩子方法 ,cleaned_data代表用户输入的全部的值
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError("格式错误")
        # 验证通过，返回用户的值
        return txt_mobile

class PrettyEditModelForm(bootstrapform):
    # 设置手机号不能编辑
    # mobile = forms.CharField(disabled=True,label='手机号')
    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    # 验证方式2
    # clean_字段名，钩子方法
    def clean_mobile(self):
        # 钩子方法 ,cleaned_data代表用户输入的全部的值
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError("格式错误")
        # 验证通过，返回用户的值
        return txt_mobile