from celery import shared_task
from .models import Text
from django.utils import timezone

@shared_task
def daily_report():
    with open("daily_report.txt", "a") as file:
        date = timezone.now().date()
        file.write(f"Report for {date}:\n")
        for text in Text.objects.all():
            labels = ", ".join([tag.name for tag in text.tags.all()])
            file.write(f"Text: {text.content[:30]}... - Tags: {labels}\n")
        file.write("\n")
