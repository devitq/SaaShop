from django.views.generic import TemplateView

__all__ = ()


class DescriptionView(TemplateView):
    template_name = "about/about.html"
