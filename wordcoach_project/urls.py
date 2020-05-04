from django.contrib import admin
from django.urls import path
from engkis import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('learn', views.learn, name='learn'),
    path('add', views.add, name='add'),
    path('adddone', views.adddone, name='adddone'),
    path('addcombinedone', views.addcombinedone, name='addcombinedone'),
    path('checkcorrect', views.checkcorrect, name='checkcorrect'),
    path('checknotcorrect', views.checknotcorrect, name='checknotcorrect'),
    path('login/', views.loginuser, name = 'loginuser'),
    path('logout/', views.logoutuser, name = 'logoutuser'),






    ]
