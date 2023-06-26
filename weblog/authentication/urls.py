from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login, name="login"),
    path('signup', views.register, name="register"),
    path('logout', views.logout, name="logout"),
    # path('password-reset/verify', views.password_reset, name='password_reset'),
    # path('reset-password/reset', views.reset_password, name='reset_password'),

    # path('password-reset/verify', 
    #     PasswordResetView.as_view(
    #         template_name='authentication/forgot_password.html',
    #         html_email_template_name='emails/index.html'
    #     ),
    #     name='password_reset'
    # ),
    # path('password-reset/done/', PasswordResetDoneView.as_view(template_name='authentication/reset_password_done.html'),name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='authentication/reset-password.html'),name='password_reset_confirm'),
    # path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='authentication/password_complete.html'),name='password_reset_complete')
    
]