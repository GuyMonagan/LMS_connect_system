from django.test import TestCase
from rest_framework.exceptions import ValidationError
from materials.validators import YouTubeValidator


class YouTubeValidatorTestCase(TestCase):
    def setUp(self):
        self.validator = YouTubeValidator(field='video_url')

    def test_valid_youtube_url(self):
        attrs = {'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
        # не должно выбрасывать исключение
        try:
            self.validator(attrs)
        except ValidationError:
            self.fail("Validator raised ValidationError unexpectedly!")

    def test_invalid_url(self):
        attrs = {'video_url': 'https://skillbox.ru/video'}
        with self.assertRaises(ValidationError):
            self.validator(attrs)

    def test_empty_url(self):
        attrs = {'video_url': ''}
        # пустые значения должны пропускаться, если blank=True
        try:
            self.validator(attrs)
        except ValidationError:
            self.fail("Validator raised ValidationError for empty value!")
