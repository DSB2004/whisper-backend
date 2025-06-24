from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginViewSet,SignUpViewSet,ForgetPasswordViewSet,ResetPasswordViewSet,VerifyViewSet
router = DefaultRouter()
router.register(r'login', LoginViewSet, basename='login')
router.register(r'signup', SignUpViewSet, basename='signup')
router.register(r'verify', VerifyViewSet, basename='verify')
router.register(r'forget', ForgetPasswordViewSet, basename='forget')
router.register(r'reset', ResetPasswordViewSet, basename='reset')
urlpatterns = [
    path('', include(router.urls)),
]
