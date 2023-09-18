from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker

from file_processor.const import FileChecksStatus
from file_processor.const import FileStatus
from file_processor.services.validator import flake_validator
from file_processor.services.validator import validate_files


def test_success_flake_validator(settings):
    path_to_file = settings.BASE_DIR / 'file_processor/tests/services/data/flake_success.py'

    lines = flake_validator(path_to_file)

    assert not lines


def test_error_flake_validator(settings):
    path_to_file = settings.BASE_DIR / 'file_processor/tests/services/data/flake_error.py'

    lines = flake_validator(path_to_file)

    assert len(lines) == 2
    assert "F401 'this' imported but unused" in lines[0]
    assert 'W292 no newline at end of file' in lines[1]


@patch('file_processor.services.validator.notify_user.delay')
def test_validate_files(delay, db):
    user = baker.make('user.User')
    file = SimpleUploadedFile('flake_success.py', b'print("hello")')
    fp = baker.make('file_processor.FileProcessor', user=user, file=file)

    validate_files(fp.file.name)

    fp.refresh_from_db()
    assert fp.checks.count() == 1


@patch('file_processor.services.validator.notify_user.delay')
def test_validate_files_all(delay, db):
    user = baker.make('user.User')
    file = SimpleUploadedFile('flake_success.py', b'print("hello")\n')
    fp1 = baker.make('file_processor.FileProcessor', user=user, file=file, status=FileStatus.New)
    file2 = SimpleUploadedFile('flake_success.py', b'import this')
    fp2 = baker.make('file_processor.FileProcessor', user=user, file=file2, status=FileStatus.Updated)

    validate_files()

    fp1.refresh_from_db()
    fp2.refresh_from_db()
    assert fp1.checks.count() == 1
    fp1_check = fp1.checks.first()
    assert fp1_check.status == FileChecksStatus.Done
    assert fp2.checks.count() == 1
    fp2_check = fp2.checks.first()
    assert fp2_check.status == FileChecksStatus.Error


