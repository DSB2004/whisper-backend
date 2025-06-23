from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginViewSet,SignUpViewSet
router = DefaultRouter()
router.register(r'login', LoginViewSet, basename='login')
router.register(r'signup', SignUpViewSet, basename='signup')

urlpatterns = [
    path('', include(router.urls)),
]
