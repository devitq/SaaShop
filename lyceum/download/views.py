from http import HTTPStatus
import os

from django.conf import settings
from django.http import FileResponse, HttpResponse

__all__ = ()


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, "rb"), as_attachment=True)
    else:
        raise HttpResponse(status=HTTPStatus.NOT_FOUND)
