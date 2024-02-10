from functools import wraps
from rest_framework.response import Response
from subscriptions.models import Subscription
from rest_framework import status



def subscription_required(view_func):
    @wraps(view_func)
    def check_sub(request, *args, **kwargs):
        user = request.user
        try:
            subscription = Subscription.objects.get(user=user)
            if subscription.is_active:
                return view_func(request, *args, **kwargs)
            else:
                return Response({'error': 'Subscription is not active'}, status=status.HTTP_403_FORBIDDEN)
        except Subscription.DoesNotExist:
            return Response({'error': 'Subscription not found'}, status=status.HTTP_403_FORBIDDEN)
    return check_sub

