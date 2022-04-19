from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from surfaceintervalapi.views import register_user, login_user, DiveView, DiverView, SpecialtyView
from rest_framework import routers


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'dives', DiveView, 'dive')
router.register(r'divers', DiverView, 'diver')
router.register(r'specialties', SpecialtyView, 'specialty')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls',
    namespace='rest_framework')),
    path('admin/', admin.site.urls),
]