from django.core.exceptions import ValidationError
from rest_framework import serializers

def validate_file_size(file):
    max_file_size = 6000000
    if file.size > max_file_size * 1024:
        raise ValidationError("file too big bros")


def validate_id(model_class,value):
        if not model_class.objects.filter(id=value).exists():
            raise serializers.ValidationError(f'{model_class.__name__} ID is not valid, please use the correct {model_class.__name__} ID')
        return value
        