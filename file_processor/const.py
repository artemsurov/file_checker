from django.db.models import TextChoices


class FileStatus(TextChoices):
    New = 'new'
    Updated = 'updated'
    Deleted = 'deleted'
    Done = 'done'
    Error = 'error'


class FileChecksStatus(TextChoices):
    Done = 'done'
    Error = 'error'
