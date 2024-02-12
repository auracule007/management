from subscriptions.models import Subscription
from rest_framework import permissions, response, status

class SubscriptionPermission(permissions.BasePermission):
    message = 'Subscription is not active.'

    def has_permission(self, request, view):
        user = request.user
        try:
            subscription = Subscription.objects.filter(user=user, is_active=True).first()
            if not subscription:
                return False  
            return True  
        except Subscription.DoesNotExist as err:
            return False 

    def has_permission_denied(self, request, message='Subscription is not active.'):
        response_data = {'message': message}
        return response.Response(response_data, status=status.HTTP_403_FORBIDDEN)
    