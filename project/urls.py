from django.urls import path
from .import views
# from .views import PostEditView

urlpatterns = [
    path("",views.projectList,name = 'project-list'),
    path("project-detail/<int:pk>/",views.projectDetail,name = 'project-detail'),
    path("edit/<int:pk>/",views.projectEdit,name = 'project-edit'),
    path('delete/<int:pk>/', views.projectDelete, name='project-delete'),
    path('comment/delete/<int:pk>/', views.commentDelete, name='comment-delete'),
    path('profile/<int:pk>/', views.profile, name='profile'),
]