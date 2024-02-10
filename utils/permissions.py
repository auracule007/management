from subscriptions.models import Subscription
from rest_framework import permissions


class SubscriptionPermission(permissions.BasePermission):
    message = 'Subscription is not active.'

    def has_permission(self, request, view):
        user = request.user
        try:
            subscription = Subscription.objects.filter(user=user).first()
            return subscription.is_active
        except Subscription.DoesNotExist:
            return False
        
        