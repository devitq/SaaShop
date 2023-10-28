from django.shortcuts import render

__all__ = ()


def item_list(response):
    return render(
        request=response,
        template_name="catalog/item_list.html",
        context={},
    )


def item_detail(response, item_id):
    return render(
        request=response,
        template_name="catalog/item.html",
        context={},
    )


def re_item_detail(response, item_id):
    return render(
        request=response,
        template_name="catalog/item.html",
        context={},
    )


def convert_item_detail(response, item_id):
    return render(
        request=response,
        template_name="catalog/item.html",
        context={},
    )
