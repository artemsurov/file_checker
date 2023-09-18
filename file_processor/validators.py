from rest_framework.exceptions import ValidationError


class ValidateFileType:
    requires_context = True

    def __call__(self, value, context):
        if not value.name.endswith('.py'):
            raise ValidationError('File extension miss match')
