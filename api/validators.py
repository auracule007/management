from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_file_size = 6000000
    if file.size > max_file_size * 1024:
        raise ValidationError("file too big bros")
