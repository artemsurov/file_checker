from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response

from file_processor import models
from file_processor.serializers import FileProcessorSerializer


class FileProcessorViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.FileProcessor.objects.all()
    serializer_class = FileProcessorSerializer

    def detail_post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

