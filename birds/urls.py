from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'birds'
# Views index
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:project_dir>/', views.project, name='project'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)