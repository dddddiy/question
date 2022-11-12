"""
程序名：后台接口url配置
功能：后台接口url配置
"""
from django.contrib import admin
from django.urls import path

from myAdmin import designView,answerView
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('api/design',designView.opera),#问卷设计者操作
    path('api/answer',answerView.opera),#问卷回答者操作
    path(r'home/', TemplateView.as_view(template_name="index.html")),
    path(r'', TemplateView.as_view(template_name="index.html")),
    path(r'index/', TemplateView.as_view(template_name="index.html")),
    path(r'login/', TemplateView.as_view(template_name="index.html")),
    path(r'register/', TemplateView.as_view(template_name="index.html")),
    path(r'resetpass/', TemplateView.as_view(template_name="index.html")),
    path(r'display.*', TemplateView.as_view(template_name="index.html")),
    path(r'thankyou/', TemplateView.as_view(template_name="index.html")),

]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
