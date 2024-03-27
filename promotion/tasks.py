from datetime import datetime
from celery import shared_task
from django.db import transaction
from .models import *
import logging

logger = logging.getLogger(__name__)


@shared_task
@transaction.atomic
def promotion_prices(reduction_amount, obj_id):
    promotions = Promotion.courses_on_promotion.through.objects.filter(
        promotion_id=obj_id
    )
    reduction = reduction_amount / 100
    try:

        for promo in promotions:
            if promo.price_override == False:
                course_price = promo.course.price
                logger.info(course_price)
                new_price = course_price - (course_price * reduction)
                logger.info(new_price)
                promo.promo_price = new_price
                promo.save()
    except Exception as e:
        logger.error("Failed:", e)


@shared_task
@transaction.atomic
def promotion_management():
    promotions = Promotion.objects.filter(is_schedule=True)
    now = datetime.now().date()
    try:
        for promotion in promotions:
            if promotion.is_schedule:
                if promotion.promo_end < now:
                    promotion.is_active = False
                    promotion.is_schedule = False
                else:
                    if promotion.promo_start <= now:
                        promotion.is_active = True
                    else:
                        promotion.is_active = False
            promotion.save()
            logger.info("Promotion saved successfully")
    except Exception as e:
        logger.error("Failed:", e)
