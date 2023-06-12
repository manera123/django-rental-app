from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [

    path('accounts/profile/', views.profile_details, name='profile'),
    path('accounts/profile/archived', views.profile_details_archived, name='profile_archived'),
    path('accounts/profile/favorites', views.profile_details_favorites, name='profile_favorites'),

    path('accounts/profile/reservations', views.profile_details_user_reservations, name='profile_reservations'),
    path('accounts/profile/reservations/ended', views.profile_details_user_reservations_ended, name='profile_reservations_ended'),
    path('accounts/profile/reservations/requests', views.profile_reservation_requests, name='profile_reservation_requests'),
    path('accounts/profile/reservations/requests/in-progress', views.profile_reservation_requests_progress, name='profile_reservation_requests_progress'),
    path('accounts/profile/reservations/requests/accepted', views.profile_reservation_requests_accepted, name='profile_reservation_requests_accepted'),
    path('accounts/profile/reservations/requests/canceled', views.profile_reservation_requests_canceled, name='profile_reservation_requests_canceled'),
    path('accounts/profile/reservations/requests/ended', views.profile_reservation_requests_ended, name='profile_reservation_requests_ended'),
    
    path('accounts/manager/control-panel', views.manager_control_panel, name='manager_control_panel'),
    path('accounts/manager/control-panel/advts/approved', views.manager_control_panel_advts_approved, name='manager_control_panel_advts_approved'),
    path('accounts/manager/control-panel/documents/requests', views.manager_control_panel_document_check_requests, name='manager_control_panel_documents_req'),
    path('accounts/manager/control-panel/documents/approved', views.manager_control_panel_documents_approved, name='manager_control_panel_documents_approved'),


    path('accounts/profile/edit', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('accounts/signup/', views.SignupView.as_view(), name='signup'),
    path("accounts/login/", auth_views.LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("activate/<uidb64>/<token>", views.activate, name='activate'),
    path(
        'accounts/reset_password/',
        views.PasswordResetView.as_view(),
        name="reset_password"),
    path(
        'accounts/reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset/password_reset_sent.html"),
        name='password_reset_done'),
    path(
        'accounts/reset/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm"),
    path(
        'accounts/reset/done',
         auth_views.PasswordResetCompleteView.as_view(
         template_name="accounts/password_reset/password_reset_done.html"),
         name="password_reset_complete"),
]
