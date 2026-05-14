from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from image.models import Image


class ImageDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, image_id):
        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response(
                {"detail": "Image not found."}, status=status.HTTP_404_NOT_FOUND
            )

        response = HttpResponse(image.blob, content_type=image.mime_type)
        response["Content-Length"] = len(image.blob)
        return response
