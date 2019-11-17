from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .views import UserList, ProjectList, RightList, IdentificationList
from .views import UserDetail, ProjectDetail, RightDetail
from .views import RecordTagList, RecordRandom
from .views import ProjectListView, ProjectTagView, ProjectDetailView
from . import views

app_name = 'birds'

# Apps views
apps_urls = [
    path('', ProjectListView.as_view(), name='project-list-view'),
    # path('projects/<int:project_id>/', ProjectDetailView.as_view(), name='project-detail-view'),
    path('<slug:project_dir>/', ProjectTagView.as_view(), name='project-tag-view'),
    path('<slug:project_dir>/edit/', ProjectDetailView.as_view(), name='project-detail-view'),
    # path('<slug:project_dir>/', views.project, name='project'),

]

# Authentication views
auth_urls = [
    path('signup/', views.signup, name='signup'), #views.SignUp.as_view()
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
	path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),   # override default logout from django.contrib.auth.urls
	path('password_reset/', auth_views.PasswordResetView.as_view(success_url='done/'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<slug:uidb64>/<slug:token>/', auth_views.PasswordResetConfirmView.as_view(success_url='../../done/'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('', include('django.contrib.auth.urls')),  # login, logout, password_change, password_change_done, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
    # path('logged_user/', views.get_logged_user, name='logged-user-data'),
    path('profile/', views.profile, name='profile'),
]

# Rest API views
rest_urls = [
    # path('users/', UserList.as_view(), name='user-list'),
    # path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('projects/', ProjectList.as_view(), name='project-list'),
    # path('projects/<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    path('projects/<slug:directory>/', ProjectDetail.as_view(), name='project-detail'),
    path('rights/', RightList.as_view(), name='right-list'),
    path('rights/<int:pk>/', RightDetail.as_view(), name='right-detail'),
    path('tags/<slug:project_dir>/<int:record_id>/', RecordTagList.as_view(), name='project-record-tag-list'),
    path('records/<slug:project_dir>/random/', RecordRandom.as_view(), name='project-record-random'),
    path('identifications/<slug:project_dir>/', IdentificationList.as_view(), name='project-identification-list'),
    # path('identifications/<int:pk>/', IdentificationDetail.as_view(), name='identification-detail'),
]

# Views index
urlpatterns = [
    path('', include(apps_urls)),
    path('accounts/', include(auth_urls)),
    path('rest_api/', include(rest_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)