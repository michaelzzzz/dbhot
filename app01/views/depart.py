from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination

def depart_list(request):
    '''部门列表'''
    # 去数据库中获取所有的部门列表
    # [对象, 对象, 对象]
    queryset = models.Deparament.objects.all()
    page_object = Pagination(request, queryset, page_size=10)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request, 'depart_list.html', context)


def depart_add(request):
    if request.method == "GET":
        return render(request, 'depart_add.html')

    # 获取用户通过post提交过来的数据
    title = request.POST.get("title")

    # 保存到数据库
    models.Deparament.objects.create(title=title)

    # 重定向回部门列表
    return redirect("/depart/list/")


def depart_delete(request):
    '''删除部门'''
    # 获取ID
    # http://127.0.0.1:8000/depart/delete/?nid=1
    nid = request.GET.get("nid")
    # 删除
    models.Deparament.objects.filter(id=nid).delete()
    # 跳转回列表
    return redirect("/depart/list/")


def depart_edit(requset, nid):
    """修改部门"""
    # 根据nid,获取他的数据[obj,]
    if requset.method == "GET":
        row_object = models.Deparament.objects.filter(id=nid).first()

        return render(requset, 'depart_edit.html', {"row_object": row_object})
    # 获取用户提交的标题
    title = requset.POST.get("title")
    # 根据ID找到数据库找到数据库中的数据并进行更新
    models.Deparament.objects.filter(id=nid).update(title=title)

    # 重定向回部门列表
    return redirect("/depart/list/")