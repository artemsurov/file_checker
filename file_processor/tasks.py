from conf import celery_app

from file_processor.services.validator import validate_files


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, cron_validate_files.s(), name='add every 10')


@celery_app.task
def cron_validate_files():
    validate_files()
