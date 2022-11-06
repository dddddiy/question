from django.utils.deprecation import   MiddlewareMixin
from django.shortcuts import render, HttpResponse, redirect
class M1(MiddlewareMixin):
    def process_request(self,request):
        if request.path_info=="/login/":
            return
        if request.path_info in ["/signin/","/img/code/"]:
            return

        info=request.session.get("info")
        if  info:
            return
        return redirect("/login/")

        print("go ")
    def process_response(self,request,response):
        print("out")
        return response