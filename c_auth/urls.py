from . import views
from django.urls import path

urlpatterns = [
    path('signup/', view=views.regster_customer, name='register_email'),
    path('signup/validate-email/', view=views.validate_email, name='validate_email'),
    path('signup/verify-email/', view=views.verify_email, name='verify_email'),
    path('signup/create-token/', view=views.create_token, name='create_token'),
    path('signup/verify-email-token/', view=views.verify_email_token, name='verify_email'),
    path('signup/resend-verification/', view=views.resend_verification, name='resend_verification'),
    path('login/', view=views.CustomTokenObtainnPairView.as_view(), name='login'),
    path('refresh/', view=views.CustomTokenRefreshView.as_view(), name='refresh_token'),
    path('logout/', view=views.CustomLogoutView.as_view(), name='logout'),
]