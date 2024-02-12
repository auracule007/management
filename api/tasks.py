from django.db import transaction
from celery import shared_task
from datetime import date, datetime
from .models import Courses
import logging

logger = logging.getLogger(__name__)


@shared_task
@transaction.atomic
def check_course_start_date():
    today = date.today()
    courses = Courses.objects.filter(set_start_date=today, is_started=False)
    for course in courses:
        if course.set_start_date == today:
            course.is_started = True
            try:
                course.save()
                logger.info("Successfully update the instance to True")
            except Exception as e:
                logger.info("Failed:", e)
        else: 
            course.is_started = False
            try:
                course.save()
                logger.info("Successfully update the instance to Falsenn             n")
            except Exception as e:
                logger.error("Failed:", e)
