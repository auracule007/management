from django.db import IntegrityError, transaction
from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone
from subscriptions.emails import send_expiration_email, send_expiring_soon_email
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
            logger.error("Failed to deactivate subscription: ", e)
        except Exception as e:
            logger.error("Failed:", e)


@shared_task
@transaction.atomic
def check_expiration_notification():
    try:
        today = datetime.now(timezone.utc)
        expiring_subscriptions = Subscription.objects.filter(
            expiration_date__gte=today,
            expiration_date__lt=today + timedelta(days=3),
        )
        for subscription in expiring_subscriptions:
            if subscription.expiration_date == today:
                send_expiration_email(subscription)
            else:
                send_expiring_soon_email(subscription)
    except Exception as err:
        logger.error("Error sending email notification: ", err)
