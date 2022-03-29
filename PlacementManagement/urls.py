
from re import template
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static #add this
from PlacementManagement import settings
from Manager.views import Login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('student',include('student.urls')),
    path('Manager',include('Manager.urls')),
    path('Login',Login),
    path('ForgotPassword/', auth_views.PasswordResetView.as_view( template_name = 'password_reset_form.html'), name="reset_password"),
    path('ResetLink/', auth_views.PasswordResetDoneView.as_view( template_name ='password_reset_email.html'), name="password_reset_done"),
    path('ResetPassword/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'pasword_reset_confirm.html'), name="password_reset_confirm"),
    path('ResetComplete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
