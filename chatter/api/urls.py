from .views import DialogViewSet, MessageListViewSet
from rest_framework import routers
from django.urls import path, include


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'chat', DialogViewSet)


app_name='chatter_api'
urlpatterns = [
    path("", include(router.urls)),
    path('message/', MessageListViewSet.as_view(), name='message'),
]
