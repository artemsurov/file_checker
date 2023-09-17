from django.db import models

from file_processor.const import FileChecksStatus
from file_processor.const import FileStatus
from file_processor.services.validator import flake_validator


class FileProcessor(models.Model):
    file = models.FileField()
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    last_check = models.DateField(null=True)
    status = models.TextField(choices=FileStatus.choices)

    def validate_file(self):
        results = flake_validator(str(self.file))
        Checks.objects.create(self, status=FileChecksStatus.Done, result=results)


class Checks(models.Model):
    file = models.ForeignKey(FileProcessor, on_delete=models.CASCADE, related_name='checks')
    date = models.DateField(auto_now_add=True)
    status = models.TextField(choices=FileChecksStatus.choices)
    result = models.TextField()
