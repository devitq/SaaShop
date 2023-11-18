from django.conf import settings
from django.http import FileResponse, HttpResponseNotFound
from django.views import View

__all__ = ()


class DownloadView(View):
    def get(self, request, path):
        if settings.STORAGE_NAME == "aws":
            return self.serve_from_s3(path)
        return self.serve_from_local(path)

    def serve_from_s3(self, path):
        import boto3

        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        try:
            s3_response = s3.get_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=settings.AWS_LOCATION + path,
            )
        except Exception as e:
            return HttpResponseNotFound(f"File not found: {e}")

        response = FileResponse(
            s3_response["Body"],
            content_type="application/octet-stream",
        )
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{path.split("/")[-1]}"'
        return response

    def serve_from_local(self, path):
        file_path = settings.MEDIA_ROOT / path
        if file_path.exists():
            return FileResponse(open(file_path, "rb"), as_attachment=True)
        return HttpResponseNotFound("File not found")
