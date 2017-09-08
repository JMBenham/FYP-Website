from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

"""
URL Patterns for the website.

index
register
about
completesurvey
profile
device_profile

"""

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^about/$', views.about, name='about'),
    url(r'^completesurvey/$', views.complete_survey, name='completesurvey'),
    url(r'^profile/(?P<id>\d+)/$', views.profile, name='profile'),
    url(r'^profileupdate/(?P<id>\d+)/$', views.UserUpdateView.as_view(), name='profileupdate'),
    url(r'^hardware/(?P<id>\d+)/$', views.device_profile, name='device_profile'),
    url(r'^deletesurvey/(?P<id>\d+)/$', views.delete_survey, name='delete_survey'),
    url(r'^login/$',
        auth_views.LoginView.as_view(template_name='website/login.html'),
        name='login'),
    url(r'^logout/$',
        auth_views.LogoutView.as_view(template_name='website/logout.html'), name='logout'),
    url(r'^password/reset/$',
        auth_views.PasswordResetView.as_view(template_name='customRegistration/password_reset_form.html'),
        name='password_reset'),
    url(r'^password/reset/confirm$',
        auth_views.PasswordResetConfirmView.as_view(template_name='customRegistration/password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^password/reset/done',
        auth_views.PasswordResetDoneView.as_view(template_name='customRegistration/password_reset_done.html'),
        name='password_reset_done'),
    url(r'^password/reset/complete$',
        auth_views.PasswordResetCompleteView.as_view(template_name='customRegistration/password_reset_complete.html'),
        name='password_reset_complete'),
    url(r'^password/change/$',
        auth_views.PasswordChangeView.as_view(template_name='customRegistration/password_change_form.html'),
        name='password_change'),
    url(r'^password/change/done$',
        auth_views.PasswordChangeDoneView.as_view(template_name='customRegistration/password_change_done.html'),
        name='password_change_done'),
]