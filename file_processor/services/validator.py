import io
import logging
from contextlib import redirect_stdout
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
        raise FileNotFoundError()
    with redirect_stdout(io.TextIOWrapper(io.BytesIO())) as f:
        cli.main([str(file)])
    f.seek(0)
    return f.readlines()


def validate_files():
    for fp in FileProcessor.objects.filter(status=Q(FileStatus.New) | Q(FileStatus.Updated)):
        results = flake_validator(str(fp.file))
        Checks.objects.create(fp, status=FileChecksStatus.Done, result=results)
        notify_user.delay(fp.user.email, fp.file.name, results)
        file_checker.info(f'File {fp.file.name} has been validated with results: {results}')
