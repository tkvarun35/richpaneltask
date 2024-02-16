from django.urls import path,include

from .import views

urlpatterns=[
    path('signIn/',views.signin),
    path('createUser/',views.createUser),
    path('syncUser/',views.syncuser),
    path('logout/',views.logout),
    path('delete/',views.delete),
    path('getAccessToken/',views.getaccess),
    path('addpage/',views.addpage),
    path('getmessage/',views.getmessage),
    path('getChat/',views.getchat),
    path('reply/',views.reply),
    path('disconnect/',views.disconnect)
    # path('getProf/',views.getprof)




]