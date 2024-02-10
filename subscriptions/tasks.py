from django.db import IntegrityError, transaction
from celery import shared_task
from datetime import datetime, date
from django.utils import timezone
from subscriptions.models import Subscription
import logging

logger = logging.getLogger(__name__)


@shared_task
@transaction.atomic
def check_sub_expiration():
    today = datetime.now(timezone.utc)
    subs_to_update = Subscription.objects.filter(expiration_date=today, is_active=True)

    for sub in subs_to_update:
        sub.is_active = False
        try:
            sub.save()
            logger.info("Successfully update the instance")
        except IntegrityError as e:
            logger.error('Failed to deactivate subscription: ', e)
        except Exception as e:
            logger.error("Failed:", e)
