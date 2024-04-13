from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.forms import PrettyEditModelForm, PrettyModelForm

def pretty_list(request):
    """靓号列表"""
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    # select * from 表 order by level desc
    # queryset = models.PrettyNum.objects.all().order_by("-level")
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'pretty_list.html', context)

def pretty_add(request):
    """添加靓号"""
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {"form": form})
    # 用户POST提交数据，数据校验。
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        form.save()
        # print(form.cleaned_data)
        return redirect("/pretty/list")
    else:
        # 校验失败（在页面上显示错误信息）
        # print(form.errors)
        return render(request, 'pretty_add.html', {"form": form})

def pretty_edit(request, nid):
    # 编辑用户
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据id去数据库要编辑的那一行数据
        # instance=row_object 告诉数据更新到哪里
        form = PrettyEditModelForm(instance=row_object)
        return render(request, "pretty_edit.html", {'form': form})
    else:
        form = PrettyEditModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            # 默认保存的是用户输入的所有数据，如果想要再用户输入意外增加一点值
            # form.instance.字段名 = 值
            # 比如说埋点
            form.save()
            return redirect('/pretty/list')
    return render(request, 'pretty_edit.html', {'form': form})

def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list")