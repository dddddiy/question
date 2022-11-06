
from django.shortcuts import render, HttpResponse, redirect
from django import forms
from app1.models import user
from app1 import models
from app1.utils.code import check_code
from io import BytesIO

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
class formlog(forms.Form):
    name=forms.CharField(label="用户名",widget=forms.TextInput,required="TRUE")
    pwd=forms.CharField(label="密码",widget=forms.PasswordInput,required="TRUE")
    code=forms.CharField(label="验证码",widget=forms.TextInput,required=True)
def login(request):

    if request.method == "GET":
        form = formlog()
        return render(request,"login.html",{'form':form})
    form = formlog(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data.get('name'))

        uucode=form.cleaned_data.pop('code')
        iicode=request.session.get('code',"")
        if uucode.upper()!=iicode.upper():
            form.add_error("code", "验证码错误")
            return render(request, "login.html", {'form': form})
        obj = models.user.objects.filter(**form.cleaned_data).first()
        if not obj:
             # print(form.cleaned_data)
             form.add_error("pwd","用户名或密码错误")
             return render(request, "login.html", {'form': form})
        request.session["info"]= {'id':obj.id, 'name':obj.name}
        request.session.set_expiry(60*60)
        return redirect("/link/")
    return render(request,"login.html",{'form':form})
        # user = request.POST.get("user")
        # print(user)
        # if user== 'root':
        #     #return HttpResponse("welcome")
        #     return redirect("https://www4.bing.com")
        # else:
        #     return render(request, "login.html", {"error":"错误"})


class myform(forms.ModelForm):
    name=forms.CharField(min_length=3,label="用户名")
    pwd = forms.CharField(min_length=3, label="密码")
    class Meta:
        model =models.user
        fields=["name","pwd"]

def signin(request):
    if request.method=="GET":
        form=myform()
        return render(request, "signin.html",{"form":form})
    else:
        form=myform(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return render("login.html")
        else:
            print(form.errors)
        return render(request, "signin.html", {"form": form})
        # user=request.POST.get("name")
        # pwd=request.POST.get("pwd")
        # sure=request.POST.get("pwd2")
        # p=models.user.objects.filter(name=user)
        # if any(p):
        #     return  HttpResponse("用户名已存在")
        # # elif sure !=pwd:
        # #     return HttpResponse("两次密码不同")
        # else:
        #     models.user.objects.create(name=user,pwd=pwd)
        #     return HttpResponse("successful")
def link(request):
    return render(request,"test.html")
def logout(request):
    request.session.clear()
    return redirect('/login/')
def code(request):
    img,code=check_code()
    st=BytesIO()
    request.session['code']=code
    request.session.set_expiry(60)
    img.save(st,'png')
    return  HttpResponse(st.getvalue())


