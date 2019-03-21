from django.urls import path
from . import views

app_name = 'birds'
# Views index
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:project_dir>/', views.project, name='project'),
]