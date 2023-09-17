import pytest
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture()
def upload_file(settings, tmp_path):
    settings.MEDIA_ROOT = str(tmp_path)
    return SimpleUploadedFile("file.py", b"import this", content_type="text/plain")
