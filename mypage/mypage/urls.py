"""mypage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import myresume.views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',myresume.views.index, name='index'),
    path('admin/', admin.site.urls),
    path('main/', myresume.views.main, name='main'),
    path('profile/', myresume.views.profile, name='profile'),
    path('stackMain/', myresume.views.stackMain, name='stackMain'),
    path('detail/<int:stack_id>/', myresume.views.detail, name='detail'),
    path('stackMain/createStack/', myresume.views.createStack, name='createStack'),
    path('detail/<int:stack_id>/updateStack/', myresume.views.updateStack, name='updateStack'),
    path('detail/<int:stack_id>/deleteStack/', myresume.views.deleteStack, name='deleteStack'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)