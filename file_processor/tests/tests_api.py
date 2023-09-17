import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from rest_framework import status

from file_processor.const import FileChecksStatus
from file_processor.const import FileStatus
from file_processor.models import FileProcessor


def test_read_files(customer_client):
    file1 = baker.make('file_processor.fileprocessor', user=customer_client.user)
    baker.make('file_processor.checks', file=file1, status=FileChecksStatus.Error)

    file2 = baker.make('file_processor.fileprocessor', user=customer_client.user)
    baker.make('file_processor.checks', file=file2, status=FileChecksStatus.Done)

    response = customer_client.get('/files/')

    assert response.status_code == status.HTTP_200_OK, response.data


def test_post_file(customer_client, upload_file):

    response = customer_client.post('/files/', data={'file': upload_file})

    assert response.status_code == status.HTTP_201_CREATED, response.data
    file = FileProcessor.objects.get(id=response.data['id'])
    assert file.status == FileStatus.New


def test_post_file_with_wrong_extension(customer_client, upload_file):

    response = customer_client.post('/files/', data={'file': upload_file})

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.data
    assert {'file': ['File extension miss match']} == response.data


def test_update_file(customer_client, upload_file):
    file1 = baker.make('file_processor.fileprocessor', user=customer_client.user, file=upload_file)
    baker.make('file_processor.checks', file=file1, status=FileChecksStatus.Error)
    new_file = SimpleUploadedFile("file.py", b"import os", content_type="text/plain")

    response = customer_client.put(f'/files/{file1.id}/', data={'file': new_file})

    assert response.status_code == status.HTTP_200_OK, response.dataa
    assert response.data['status'] == FileStatus.Updated


def test_delete_file(customer_client):
    file = baker.make('file_processor.fileprocessor', user=customer_client.user)

    response = customer_client.delete(f'/files/{file.id}/')

    assert response.status_code == status.HTTP_204_NO_CONTENT, response.data
    file.refresh_from_db()
    assert file.status == FileStatus.Deleted


def test_run_checks_success(customer_client, upload_file):
    file = baker.make('file_processor.fileprocessor', user=customer_client.user, file=upload_file)

    response = customer_client.post(f'/files/{file.id}/')

    assert response.status_code == status.HTTP_200_OK, response.data


def test_run_checks_fail(customer_client, upload_file):
    file = baker.make('file_processor.fileprocessor', file=upload_file)

    response = customer_client.post(f'/files/{file.id}/')

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.data



