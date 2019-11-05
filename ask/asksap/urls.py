"""asksap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from askqa import views

urlpatterns = [
    path('', views.index, name='askqa_index'),
    path('hot/', views.hot, name='askqa_hot'),
    path('tag/<str:tag_name>', views.tag, name="askqa_tag"),
    path('login/', views.login, name='askqa_login'),
    path('signup/', views.signup, name='askqa_signup'),
    path('question/<int:question_id>', views.question, name='askqa_question'),
    path('ask/', views.ask, name='askqa_ask'),
    path('profile/', views.profile, name='askqa_profile'),
    path('logout/', views.logout, name='askqa_logout'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
