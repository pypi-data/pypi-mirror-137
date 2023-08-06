# -*- coding: utf-8 -*-
from django.urls import re_path
from rest_framework import routers

from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from xdj_oauth.views import BasicAuthViewSet,WXAcAuthViewSet,WXMiniAuthViewSet

system_url = routers.SimpleRouter()

urlpatterns = format_suffix_patterns([

    path('check/wx_ac/', WXAcAuthViewSet.as_view({'get': 'auth_check','post': 'auth_check'})),
    path('code/wx_ac/', WXAcAuthViewSet.as_view({'get': 'code'})),
    path('wx_ac/', WXAcAuthViewSet.as_view({'get': 'auth', 'post': 'auth'})),
    path('wx_mini/', WXMiniAuthViewSet.as_view({'post': 'auth'})),
    path('basic/', BasicAuthViewSet.as_view({'post': 'auth'})),
    # 其他接口
])
urlpatterns += system_url.urls
