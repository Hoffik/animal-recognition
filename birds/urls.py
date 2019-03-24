from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

from .views import ProjectList, ProjectDetail
from .views import ProjectListView
from . import views

app_name = 'birds'

# Apps views
apps_urls = [
    path('', ProjectListView.as_view(), name='project-list-view'),
    path('<slug:project_dir>/', views.project, name='project'),
]

# Rest API views
rest_urls = [
    path('projects/', ProjectList.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
]

# Views index
urlpatterns = [
    path('', include(apps_urls)),
    path('rest_api/', include(rest_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)