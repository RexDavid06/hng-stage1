from django.urls import path
from . import views

urlpatterns = [
    # Create new string
    path("strings/create/", views.CreateStringView.as_view(), name="create_string"),

    # List all strings
    path("strings/", views.StringListView.as_view(), name="list_strings"),

    #  Delete a specific string by value
    path("strings/<path:string_value>/", views.DeleteStringView.as_view(), name="delete_string"),
]
