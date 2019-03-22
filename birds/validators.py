from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

# def validate_keywords(keywords):
#     if not ".edu" in value:
#         raise ValidationError("A valid school email must be entered in")
#     else:
#         return value

@deconstructible
class KeywordValidator(object):
    keywords = []
    
    def __init__(self, keyword_list=None):
        if keyword_list is not None:
            self.keywords = keyword_list

    def __call__(self, value):
        for keyword in self.keywords:
            if value == keyword:
                raise ValidationError('A project dir cannot be a "' + value + '" keyword')
        return value