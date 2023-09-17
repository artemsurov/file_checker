from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker

from file_processor.models import FileProcessor
from file_processor.services.validator import flake_validator


def test_success_validate_file():
    path_to_file = './data/flake_success.py'

    lines = flake_validator(path_to_file)

    assert not lines


def test_error_validate_file():
    path_to_file = './data/flake_error.py'

    lines = flake_validator(path_to_file)

    assert len(lines) == 2
    assert "data/flake_error.py:1:1: F401 'this' imported but unused\n" in lines
    assert 'data/flake_error.py:1:12: W292 no newline at end of file\n' in lines


def test_model_validate_file(upload_file):
    file = baker.make('file_processor.fileprocessor', file=upload_file)

    file.validate_file()
