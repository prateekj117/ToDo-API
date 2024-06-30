from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from todo import views

schema_view = get_schema_view(
   openapi.Info(
      title="TODO API Docs",
      default_version='v1',
      description="Docs for rest api's in the project",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="prateekj1171998@gmail.com"),
      license=openapi.License(name="Awesome License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("users/", include("authentication.urls")),
    path('tasks', views.TaskRegistrationView.as_view(), name='tasks'),
    path('tasks/<str:pk>', views.TaskDetailView.as_view(), name="tasks-Detail"),
]
