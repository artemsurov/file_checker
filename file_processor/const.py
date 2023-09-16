from django.db.models import TextChoices


class FileStatus(TextChoices):
    New = 'new'
    Updated = 'updated'
    Deleted = 'deleted'


class FileChecksStatus(TextChoices):
    Done = 'done'
    Error = 'error'
