from django.urls import path
from . import views

urlpatterns = [
    path("strings/", views.StringListView.as_view(), name="list_strings"),  # GET /strings
    path("strings/create/", views.CreateStringView.as_view(), name="create_string"),  # POST /strings/create
    path("strings/delete/<path:string_value>/", views.DeleteStringView.as_view(), name="delete_string"),  # DELETE /strings/delete/{value}
    path("strings/filter-by-natural-language", views.NaturalLanguageFilterView.as_view(), name="nl_filter"),  # GET /strings/filter-by-natural-language
    path("strings/<path:string_value>/", views.RetrieveStringView.as_view(), name="get_string"),  # GET /strings/{value}
]
