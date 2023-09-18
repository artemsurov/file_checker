from celery import shared_task

from file_processor.services.validator import validate_files


@shared_task(name='validate_files_task')
def validate_files_task(file_name: str = ''):
    validate_files(file_name)
