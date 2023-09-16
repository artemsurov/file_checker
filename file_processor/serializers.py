from rest_framework import serializers
from rest_framework import fields
from rest_framework.fields import CharField
from rest_framework.fields import Field
from rest_framework.fields import empty

from file_processor import models
from file_processor.const import FileStatus
from file_processor.validators import ValidateFileType


class ChecksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Checks
        fields = (
            'date',
            'status',
            'result',
        )


class StatusField(CharField):  # CharField

    def get_value(self, dictionary):
        if not self.parent.instance:
            return FileStatus.New
        return FileStatus.Updated


class FileProcessorSerializer(serializers.ModelSerializer):
    user = fields.HiddenField(default=fields.CurrentUserDefault())
    checks = ChecksSerializer(read_only=True, many=True)
    status = StatusField()

    class Meta:
        model = models.FileProcessor
        fields = (
            'id',
            'file',
            'user',
            'last_check',
            'status',
            'checks',
        )
        extra_kwargs = {
            'last_check': {'read_only': True},
            'file': {'validators': [ValidateFileType()]}
        }


