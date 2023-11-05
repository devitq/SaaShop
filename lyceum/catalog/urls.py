from django.urls import path, re_path, register_converter

from catalog import converters, views

register_converter(converters.PositiveIntengerConverter, "int_positive")


app_name = "catalog"
urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("new/", views.new_item_list, name="new_item_list"),
    path("friday/", views.friday_item_list, name="friday_item_list"),
    path(
        "unverified/",
        views.unverified_item_list,
        name="unverified_item_list",
    ),
    path("<int:item_id>/", views.item_detail, name="item_detail"),
    re_path(
        r"^re/(?P<item_id>[1-9][\d*]*)/$",
        views.re_item_detail,
        name="re_item_detail",
    ),
    path(
        "converter/<int_positive:item_id>/",
        views.convert_item_detail,
        name="converter_item_detail",
    ),
]
