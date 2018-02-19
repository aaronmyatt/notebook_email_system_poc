from django.urls import path
from . import views

urlpatterns = [
    path(r'notebooks/', views.all_notebooks, name='notebooks_list')
]