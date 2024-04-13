from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.forms import UserModelForm
def user_list(request):
    """用户管理"""
    queryset = models.UserInfo.objects.all()
    page_object = Pagination(request, queryset, page_size=10)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }
    # for obj in queryset:
    #     print(obj.id, obj.name, obj.account, obj.age, obj.get_gender_display(), obj.depart.title)
    return render(request, 'user_list.html', context)

def user_add(request):
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Deparament.objects.all()
        }
        return render(request, 'user_add.html', context)
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    ac = request.POST.get('ac')
    ct = request.POST.get('ct')
    gender = request.POST.get('gender')
    dp = request.POST.get('dp')
    models.UserInfo.objects.create(name=user, password=pwd, age=age, account=ac, create_time=ct, gender=gender,
                                   depart_id=dp)
    return redirect("/user/list/")

def user_model_form_add(request):
    """添加用户（ModelForm版本的）"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form": form})

    # 用户POST提交数据，数据校验。
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        form.save()
        # print(form.cleaned_data)
        return redirect("/user/list")
    else:
        # 校验失败（在页面上显示错误信息）
        # print(form.errors)
        return render(request, 'user_model_form_add.html', {"form": form})

def user_edit(request, nid):
    # 编辑用户
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据id去数据库要编辑的那一行数据
        # instance=row_object 告诉数据更新到哪里
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {'form': form})
    else:
        form = UserModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            # 默认保存的是用户输入的所有数据，如果想要再用户输入意外增加一点值
            # form.instance.字段名 = 值
            # 比如说埋点
            form.save()
            return redirect('/user/list')
    return render(request, 'user_edit.html', {'form': form})

def user_delete(nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list")