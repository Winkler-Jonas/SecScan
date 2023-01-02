from django.urls import path

from .views import ErrorDetail, ErrorList

urlpatterns = [
    path("<int:pk>/", ErrorDetail.as_view(), name="error-detail"),
    path("", ErrorList.as_view(), name="error-list"),
]
