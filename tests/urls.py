# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


from django.urls import path, re_path, include
from django.contrib import admin
from chatter.api.urls import router

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'chat/', include('chatter.urls', namespace='chatter')),
    re_path(r'chatter_api/', include(router.urls)),
]
