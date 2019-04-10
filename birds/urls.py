from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .views import UserList, ProjectList, RightList, IdentificationList
from .views import UserDetail, ProjectDetail, RightDetail, IdentificationDetail
from .views import ProjectListView, ProjectDetailView
from . import views

app_name = 'birds'

# Apps views
apps_urls = [
    path('', ProjectListView.as_view(), name='project-list-view'),
    # path('projects/<int:project_id>/', ProjectDetailView.as_view(), name='project-detail-view'),
    path('<slug:project_dir>/edit/', ProjectDetailView.as_view(), name='project-detail-view'),
    path('<slug:project_dir>/', views.project, name='project'),

]

# Authentication views
auth_urls = [
    path('signup/', views.signup, name='signup'), #views.SignUp.as_view()
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    # path('logged_user/', views.get_logged_user, name='logged-user-data'),
    path('profile/', views.profile, name='profile'),
]

# Rest API views
rest_urls = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('projects/', ProjectList.as_view(), name='project-list'),
    # path('projects/<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    path('projects/<slug:directory>/', ProjectDetail.as_view(), name='project-detail'),
    path('rights/', RightList.as_view(), name='right-list'),
    path('rights/<int:pk>/', RightDetail.as_view(), name='right-detail'),
    path('identifications/', IdentificationList.as_view(), name='identification-list'),
    path('identifications/<int:pk>/', IdentificationDetail.as_view(), name='identification-detail'),
]

# Views index
urlpatterns = [
    path('', include(apps_urls)),
    path('accounts/', include(auth_urls)),
    path('rest_api/', include(rest_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)