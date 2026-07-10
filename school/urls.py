"""Explicit school API URL routes."""
from django.urls import path

from school.views import SchoolViewSet

school_list = SchoolViewSet.as_view({"get": "list", "post": "create"})
school_detail = SchoolViewSet.as_view({"get": "retrieve", "patch": "partial_update", "put": "update", "delete": "destroy"})
school_active = SchoolViewSet.as_view({"get": "active"})
school_search = SchoolViewSet.as_view({"get": "search"})
school_statistics = SchoolViewSet.as_view({"get": "statistics"})

urlpatterns = [
    path("schools/", school_list, name="school-list"),
    path("schools/active/", school_active, name="school-active"),
    path("schools/search/", school_search, name="school-search"),
    path("schools/statistics/", school_statistics, name="school-statistics"),
    path("schools/<int:pk>/", school_detail, name="school-detail"),
]
