from django.urls import path

from catalog import views


app_name = "catalog"
urlpatterns = [
    path(
        "",
        views.ItemListView.as_view(),
        name="item_list",
    ),
    path(
        "new/",
        views.NewItemListView.as_view(),
        name="new_item_list",
    ),
    path(
        "friday/",
        views.FridayItemListView.as_view(),
        name="friday_item_list",
    ),
    path(
        "unverified/",
        views.UnverifiedItemListView.as_view(),
        name="unverified_item_list",
    ),
    path(
        "<int:pk>/",
        views.ItemDetailView.as_view(),
        name="item_detail",
    ),
]
