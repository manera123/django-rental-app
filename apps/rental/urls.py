from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'rental'
urlpatterns = [

    path('', views.index, name='index'),
    path('advt/<int:id>', views.ad_details, name='advt'),
    path('advt/add/step/1', views.advt_add_step_1, name='advt_add_step_1'),
    path('advt/add/step/2/<int:id>', views.advt_add_step_2, name='advt_add_step_2'),
    path('advt/add/step/3/<int:id>', views.advt_add_step_3, name='advt_add_step_3'),
    path('advt/add/images/<int:id>', views.advt_add_images, name='advt_add_images'),
    path('advt/edit/<int:id>/step/1', views.advt_edit_step_1, name='advt_edit_step_1'),
    path('advt/edit/<int:id>/step/2', views.advt_edit_step_2, name='advt_edit_step_2'),
    path('advt/edit/<int:id>/step/3', views.advt_edit_step_3, name='advt_edit_step_3'),
    path('advt/edit/<int:id>/approve', views.approved_advt, name='advt_edit_approve'),
    path('advt/delete/<int:id>', views.advt_delete, name='advt_delete'),

    path('advt/edit/<int:id>/to/archive', views.advt_to_or_from_archive, name='advt_to_of_from_archive'),

    path('advt/edit/<int:id>/to/favorite', views.advt_to_favorite, name='advt_to_favorite'),
    path('advt/edit/<int:id>/from/favorite', views.advt_from_favorite, name='advt_from_favorite'),
    path('advt/documents-check', views.send_documents_for_check, name='documents_check_request'),
    path('advt/documents-check/approved/<int:id>', views.approved_documents, name='documents_approved'),
    
    path('advt/edit/<int:id>/cancel/reservation', views.advt_reservation_cancel, name='advt_reservation_cancel'), 
    path('advt/edit/<int:id>/accept/reservation', views.advt_reservation_accept, name='advt_reservation_accept'), 
    path('advt/edit/<int:id>/end/reservation', views.advt_reservation_end, name='advt_reservation_end'), 
    path('advt/edit/<int:id>/cancel-by-host/reservation', views.advt_reservation_cancel_by_host, name='advt_reservation_cancel_by_host'), 
]
