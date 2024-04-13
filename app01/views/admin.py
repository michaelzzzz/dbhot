from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.bootstrapform import bootstrapform
from django.core.exceptions import ValidationError
from app01.utils import encrypt


def admin_list(request):
    #用户发来请求，获取cookie随机字符串，拿着随机字符串看看session中有没有
    # info = request.session.get("info")
    # print(info)
    # if not info:
    #     return redirect('/login')
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__contains"] = search_data
    # queryset = models.Admin.objects.all()
    queryset = models.Admin.objects.filter(**data_dict)

    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, 'admin_list.html', context)


from django import forms


class AdminModelForm(bootstrapform):
    # 自己定义的确认密码字段
    confirm_password = forms.CharField(
        label="确认密码",
        # render_value=True 密码不清空
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        mdpwd = encrypt.md5(pwd)
        return mdpwd

    # 钩子函数
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = encrypt.md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致")
        return confirm


def admin_add(request):
    """添加管理员"""
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "change.html", {"title": title, "form": form})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')

    return render(request, 'change.html', {"title": title, "form": form})


def admin_edit(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {"msg": "数据不存在"})

    title = "编辑管理员"
    if request.method == "GET":
        form = AdminModelForm(instance=row_object)
        return render(request, 'change.html', {"title": title, 'form': form})
    form = AdminModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    return render(request, 'change.html', {"title": title, 'form': form})


def admin_delete(request, nid):
    # 删除
    models.Admin.objects.filter(id=nid).delete()
    # 跳转回列表
    return redirect("/admin/list/")


class AdminResetModelForm(bootstrapform):
    # 自己定义的确认密码字段
    confirm_password = forms.CharField(
        label="确认密码",
        # render_value=True 密码不清空
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ['password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md_pwd = encrypt.md5(pwd)
        # 去数据库校验当前密码和新输入的密码是否一致，.pk就是当前那行的id
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md_pwd).exists()
        if exists:
            raise ValidationError("密码不能和之前一致")
        return md_pwd

    # 钩子函数
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = encrypt.md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致")
        return confirm


def admin_reset(request, nid):
    """重置密码"""
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list')
    title = "重置密码-{}".format(row_object.username)
    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, 'change.html', {"title": title, 'form': form})
    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    return render(request, 'change.html', {"title": title, 'form': form})
