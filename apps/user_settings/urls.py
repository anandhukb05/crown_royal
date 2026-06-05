from django.urls import path
from . import views

urlpatterns = [
    # Settings root
    path('', views.settings_view, name='settings'),

    # Branches
    path('branches/', views.settings_branches, name='settings_branches'),
    path('branches/create/', views.branch_create, name='branch_create'),
    path('branches/<int:pk>/edit/', views.branch_edit, name='branch_edit'),
    path('branches/<int:pk>/delete/', views.branch_delete, name='branch_delete'),

    # Departments
    path('departments/', views.settings_departments, name='settings_departments'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<int:pk>/edit/', views.department_edit, name='department_edit'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),

    path('/expenses',                       views.bill_list,       name='bill_list'),
    path('add/',                   views.bill_create,     name='bill_create'),
    path('<int:pk>/',              views.bill_detail,     name='bill_detail'),
    path('<int:pk>/edit/',         views.bill_edit,       name='bill_edit'),
    path('<int:pk>/delete/',       views.bill_delete,     name='bill_delete'),
    path('<int:pk>/mark-items/',   views.bill_mark_items, name='bill_mark_items'),
]