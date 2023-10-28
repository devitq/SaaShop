from django.urls import path, re_path, register_converter

from . import converters, views

register_converter(converters.PositiveIntengerConverter, "int_positive")


app_name = "catalog"
urlpatterns = [
    path("", views.item_list, name="item_list"),
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
