import re
from rest_framework import serializers


def validate_no_special_characters(value):
    special_characters = re.compile(
        r'[<>/]'
    )

    if special_characters.search(value):
        raise serializers.ValidationError(
            "Special characters are not allowed.",
            code='invalid_characters'
        )
