from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^about/$', views.about, name='about'),
    url(r'^completesurvey/$', views.completeSurvey, name='completesurvey'),
    url(r'^profile/(?P<id>\d+)/$', views.profile, name='profile'),
    url(r'^login/$',
        auth_views.LoginView.as_view(template_name='website/login.html'),
        name='login'),
    url(r'^logout/$',
        auth_views.LogoutView.as_view(template_name='website/logout.html'), name='logout'),
]