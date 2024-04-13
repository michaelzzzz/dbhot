from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 0.排除哪些不需要登录就能访问的页面
        # request.path_info 获取当前用户请你去的url
        if request.path_info in ["/login/", "/image/code/"]:
            return
        # 1.读取当前访问的用户的session信息，如果能读到，说明已登录，可以继续向后走
        info_dict = request.session.get("info")
        # print(request.path_info)
        # print(info_dict)
        if info_dict:
            return

        # 2.如果没有登录过,重新回到登录页面
        return redirect('/login')
        # return HttpResponse("请登录")
