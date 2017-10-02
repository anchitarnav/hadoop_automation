from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'hadoopadmin/$', views.hadoopadmin, name='hadoopadmin'),
    url(r'hadoopfsck/$',views.hadoopfsck, name='hadoopfsck'),
    url(r'fileview/$',views.files_view,name='files_view'),
    url(r'filesadd/$',views.files_add,name='files_add'),
    url(r'jobview',views.jobview,name='jobview'),
    url(r'jobadd/$',views.jobadd,name='jobadd'),
    url(r'login/$',views.auth_login,name='auth_login'),
    url(r'logout/$',views.auth_logout,name='auth_logout')
]
