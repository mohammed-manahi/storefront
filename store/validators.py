from django.core.exceptions import ValidationError


def validate_image_size(file):
    # Custom validator for image size for product image model
    max_size_in_kb = 500
    if file.size > max_size_in_kb * 1024:
        raise ValidationError(f"Files can not be larger than {max_size_in_kb}KB.")
