from django.shortcuts import render, HttpResponse, redirect


# Create your views here.
# -- coding: utf-8 --**

def index(request):
    return HttpResponse("welcome")


# def web(request):
#     import requests
#     #http://www.chinaunicom.com.cn/api/article/NewsByIndex/2/2022/10/news
#     re = requests.get("http://www.chinaunicom.com.cn/api/article/NewsByIndex/2/2022/09/news")
#     da_list = re.json()
#     print(da_list)
#     return render(request, "第三问.html", {"n": da_list})
def ans(request):#request封装请求数据
    print(request.method)
    print(request.GET)
    #return redirect("https://www4.bing.com")
def login(request):
    if request.method == "GET":
        return render(request,"signin.html")
    else:
        print(request.POST)
        user = request.POST.get("user")
        print(user)
        if user== 'root':
            #return HttpResponse("welcome")
            return redirect("https://www4.bing.com")
        else:
            return render(request, "signin.html", {"error":"错误"})
