from templated_mail.mail import BaseEmailMessage
from .models import *

def send_subscription_confirmation(enrollment_id):
    try:
        subscribed = Subscription.objects.only('id').filter(enrollment_id=enrollment_id).first()
        message = BaseEmailMessage(
            template_name="subscriptions/send_subscription_confirmation.html",
            context={
                "plan_name": subscribed.enrollment.courses.name,
                "plan_price": subscribed.enrollment.courses.price,
                "plan_interval": subscribed.enrollment.interval,
                "pending_status": subscribed.pending_status,
                "start_date": subscribed.start_date,
                "expiration_date":subscribed.expiration_date,
                "transaction_id": subscribed.transaction_id
            },
        )
        message.send([subscribed.user.email])
        print("Sent")
    except Exception as e:
        print("Failed: ", e)


def send_expiration_email(subscription):
    try:
        message = BaseEmailMessage(
            template_name="subscriptions/send_expiration_email.html",
            context={
                "plan_name": subscription.plan.name,
                "plan_price": subscription.plan.price,
                "plan_interval": subscription.plan.interval,
                "pending_status": subscription.pending_status,
                "start_date": subscription.start_date,
                "expiration_date":subscription.expiration_date,
                "transaction_id": subscription.transaction_id
            },
        )
        message.send([subscription.user.email])
        print("Sent")
    except Exception as e:
        print("Failed: ", e)

  
def send_expiring_soon_email(subscription):
    try:
      message = BaseEmailMessage(
            template_name="subscriptions/send_expiring_soon_email.html",
            context={
                "plan_name": subscription.plan.name,
                "plan_price": subscription.plan.price,
                "plan_interval": subscription.plan.interval,
                "pending_status": subscription.pending_status,
                "start_date": subscription.start_date,
                "expiration_date":subscription.expiration_date,
                "transaction_id": subscription.transaction_id
            },
        )
      message.send([subscription.user.email])
      print("Sent")
    except Exception as e:
        print("Failed: ", e)