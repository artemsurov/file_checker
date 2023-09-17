from django.http import Http404
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from file_processor import models
from file_processor.const import FileStatus
from file_processor.serializers import FileProcessorSerializer


class FileProcessorViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.FileProcessor.objects.all()
    serializer_class = FileProcessorSerializer

    def perform_destroy(self, instance):
        instance.status = FileStatus.Deleted
        instance.save(update_fields=('status',))

    def detail_post(self, request, *args, **kwargs):
        try:
            instance: models.FileProcessor = self.get_object()
        except Http404:
            raise PermissionDenied({"result": "failed", "message": "have no access to this file"})
        instance.validate_file()
        return Response(status=status.HTTP_200_OK, data={"result": "ok", "message": "file under testing"})

