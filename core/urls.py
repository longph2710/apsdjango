from django.urls import path, re_path
from . import views

urlpatterns = [
    path('jobs/list', views.list_job),
    path('jobs/history', views.list_history),
    path('jobs/update/<str:id>', views.update_job),
    path('jobs/create', views.create_job),
    path('jobs/delete_all', views.delete_all_job),
    path('jobs/delete/<str:job_id>', views.delete_job),
]