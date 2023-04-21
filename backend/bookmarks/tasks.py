from celery import shared_task


@shared_task
def demo_celery_task(message: str) -> None:
    print("Celery says: " + message)
