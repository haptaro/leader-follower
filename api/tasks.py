import time
from celery import shared_task

@shared_task(bind=True)
def dummy_task(self, index: int) -> str:
    time.sleep(3)
    return f"task-{index} done"
