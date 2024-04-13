from io import BytesIO

from django.shortcuts import render, HttpResponse, redirect
from django import forms

from app01 import models
from app01.utils.bootstrapform import bootform
from app01.utils.code import check_code
from app01.utils.encrypt import md5


class LoginForm(bootform):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        # 必须填写，不能为空
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        # 必须填写，不能为空
        required=True
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        # 必须填写，不能为空
        required=True
    )

    # 钩子函数，获取password，并加密成md5
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


def login(request):
    """登录"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 写入到session里的值{'username': 'michael', 'password': '09f3431f64ded93e7504268533f0bb8e', 'code': 'HVZTV'}
        print("form.cleaned_data:{}".format(form.cleaned_data))
        # 获取用户输入的验证码
        user_input_code = form.cleaned_data.pop('code')
        # 获取图片验证码
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})
        # 数据库查询，**form.cleaned_data字典解开成为独立的元素作为形参
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {"form": form})

        # 用户名和密码正确
        # 网站生成随机字符串；写到用户浏览器的cookie中；在写入到session中；
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect('/admin/list')
    else:
        return render(request, 'login.html', {"form": form})


def image_code(request):
    """生成图片验证码"""
    img, code_string = check_code()
    print(code_string)
    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 设置验证码60S超时
    request.session.set_expiry(60)
    # 存入到内存
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """注销"""
    request.session.clear()
    return redirect("/login")
