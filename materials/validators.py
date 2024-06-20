from django.core.exceptions import ValidationError
import re


class YouTubeLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        youtube_regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')
        if not youtube_regex.match(value):
            raise ValidationError(f'Только ссылки на youtube.com разрешены в поле {self.field}.')

# def validate_youtube_link(value):
#     youtube_regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')
#     if not youtube_regex.match(value):
#         raise ValidationError('Только ссылки на youtube.com разрешены.')
