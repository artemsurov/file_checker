import io
import logging
from contextlib import redirect_stdout
import datetime
from pathlib import Path

from django.db.models import Q
from flake8.main import cli
from user.tasks import notify_user

from file_processor.const import FileChecksStatus
from file_processor.const import FileStatus
from file_processor.models import Checks
from file_processor.models import FileProcessor


file_checker = logging.getLogger('file_checker')


def flake_validator(path_to_file: str):
    file = Path(path_to_file)
    if not file.exists():
        file_checker.info('File %s not found', file.name)
        return
    with redirect_stdout(io.TextIOWrapper(io.BytesIO())) as f:
        cli.main([str(file)])
    f.seek(0)
    return f.readlines()


def validate_files(file_name: str = ''):
    if file_name:
        query = Q(file=file_name)
    else:
        query = Q(status=FileStatus.New) | Q(status=FileStatus.Updated)
    for fp in FileProcessor.objects.filter(query):
        results = flake_validator(fp.file.path)
        if results:
            status = FileChecksStatus.Error
            fp.status = FileStatus.Error
        else:
            status = FileChecksStatus.Done
            fp.status = FileStatus.Done

        fp.last_check = datetime.date.today()
        fp.save()

        Checks.objects.create(file=fp, status=status, result=results)
        notify_user.delay(fp.user.email, fp.file.name, results)
        file_checker.info('File %s has been validated with results: %s', fp.file.name, results)
