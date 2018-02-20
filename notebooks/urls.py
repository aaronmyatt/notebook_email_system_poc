from django.urls import path
from . import views

urlpatterns = [
    path(r'notebooks/', views.notebooks_list, name='notebooks_list'),
    path(r'notebooks/<str:file_name>', views.notebook2html, name='notebook2html')
]