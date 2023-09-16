from django.db import models

from file_processor.const import FileChecksStatus
from file_processor.const import FileStatus


class FileProcessor(models.Model):
    file = models.FileField()
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    last_check = models.DateField(null=True)
    status = models.TextField(choices=FileStatus.choices)


class Checks(models.Model):
    file = models.ForeignKey(FileProcessor, on_delete=models.CASCADE, related_name='checks')
    date = models.DateField(auto_now_add=True)
    status = models.TextField(choices=FileChecksStatus.choices)
    result = models.TextField()
