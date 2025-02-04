from django.utils.translation import gettext_lazy as _
from enum import Enum


class PostStatus(Enum):
    """Publication state machine with human-friendly labels"""

    DRAFT = "draft"
    PUBLISHED = "published"

    @classmethod
    def choices(cls):
        return [(cls.DRAFT.value, _("Draft")), (cls.PUBLISHED.value, _("Published"))]
