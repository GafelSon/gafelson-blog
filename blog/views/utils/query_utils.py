# views/utils/query_utils.py
from django.utils import timezone
from django.db.models import Q, QuerySet, Count
from django.db.models.functions import ExtractYear
from django.contrib.auth.models import User
from typing import Tuple, Optional
from blog.models import Post, PostStatus

class PostQueryEngine:
    """ Post filtering system with multi-dimensional access control """
    
    @staticmethod
    def get_post_years() -> QuerySet:
        """ Temporal analyzer for post publication history """
        return Post.objects.annotate(
            year=ExtractYear("published")
        ).values("year").annotate(
            count=Count("id")
        ).order_by("-year")

    @staticmethod
    def get_filtered_posts(
        user: User, 
        selected_year: Optional[str] = None
    ) -> Tuple[QuerySet[Post], QuerySet[Post]]:
        """ Secure post retrieval with quantum access filters """
        base_query = Post.objects.select_related('author')
        published_status = PostStatus.PUBLISHED.value

        pinned = base_query.filter(
            is_pinned=True,
            status=published_status,
            published__lte=timezone.now()
        )

        query_filter = Q(status=published_status)
        if not user.is_authenticated:
            query_filter &= Q(published__lte=timezone.now())
        if selected_year and selected_year.isdigit():
            query_filter &= Q(published__year=int(selected_year))

        return pinned, base_query.filter(query_filter).order_by('-published')