from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns =[
    url(r'^index/$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'accounts/index.html'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<pk>\d+)/$', views.other_profile, name='other_profile'),
    url(r'^friends/$', views.friends, name='friends'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^change-password/$', views.change_password, name='change_password'),
    url(r'^feedback/$', views.FeedBack.as_view(), name='feedback'),
    url(r'^post/$', views.MyPost.as_view(), name='post'),
    url(r'^post/comment/(?P<pk>\d+)/$', views.make_comment, name='comment'),
    url(r'^connect/(?P<op>.+)/(?P<pk>\d+)/$', views.connect, name='connect'),
]