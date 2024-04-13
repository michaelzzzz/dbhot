"""
自定义分页组件
在视图函数中
def pretty_list(request):
    #1.根据自己的情况去筛选自己的数据
    queryset = models.PrettyNum.objects.all()

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset, #分完页的数据
        "page_string": page_object.html()   #页码
    }
    return render(request, 'pretty_list.html', context)

在html页面中
        <ul class="pagination">
            {{ page_string }}
        </ul>
"""
from django.utils.safestring import mark_safe

class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page",plus=5):
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.totle_page_count = total_page_count
        self.plus = plus


    def html(self):
        # 计算出显五示当前页面的前页、后5页
        if self.totle_page_count<=2 * self.plus+1:
            start_page = 1
            end_page = self.totle_page_count
        else:
            #数据库中数据比较多 大于11页

            if self.page <=self.plus:
                start_page = 1
                end_page = 2*self.plus+1
            else:
                if (self.page+self.plus)>self.totle_page_count:
                    start_page = self.totle_page_count-2*self.plus
                    end_page = self.totle_page_count
                else:
                    start_page = self.page-self.plus
                    end_page = self.page+self.plus

        page_str_list = []
        page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
        if self.page >1:
            prev = '<li><a href="?page={}">上一页</a></li>'.format(self.page-1)
        else:
            prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
        page_str_list.append(prev)

        #页面
        for i in range(start_page,end_page+1):
            if i ==self.page:
                ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i,i)
            else:
                ele = '<li><a href="?page={}">{}</a></li>'.format(i,i)

            page_str_list.append(ele)

        #尾页
        page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(self.totle_page_count))

        search_string = """
            <li>
            <form  style="float:left;margin-left:-1px" method="get">
                <div class="input-group" style="width:200px">
                <input name="page" type="text" class="form-control" placeholder="页码">
                <span class="input-group-btn">
                <button class="btn btn-default" type="submit">Go!</button>
                </span>
                </div>
            </form>
            </li>
        """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string



