from rest_framework import serializers

class YouTubeValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)
        if value and "youtube.com" not in value:
            raise serializers.ValidationError({self.field: "Разрешены только ссылки на youtube.com"})
