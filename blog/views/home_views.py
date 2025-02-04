from django.http import HttpRequest, HttpResponse
from django.views import View
from django.utils import timezone
from django.core.cache import cache
from typing import Tuple, List, Dict, Any
from django.contrib.auth.models import User
from django.shortcuts import render

from blog.models import Post, PostStatus
from datetime import datetime, timedelta
from collections import defaultdict

from .utils import get_filtered_posts, add_post_summaries, get_post_years, get_activity_data

class HomeView(View):
    """🏠 God-tier homepage view serving knowledge with style! ✨"""
    
    _POST_YEARS_CACHE_KEY: str = 'post_years'
    _POST_YEARS_CACHE_TIMEOUT: int = 300  # ⏳ 1 hour cache lifespan
    
    def get(self, request: HttpRequest) -> HttpResponse:
        """ Handle GET requests with ninja-like efficiency """
        selected_year = self._get_selected_year(request)
        context: Dict[str, Any] = {
            **self._get_post_data(request, selected_year),
            **self._get_user_data(request),
            **self._get_activity_data(selected_year),
        }
        return render(request, "index.html", context)
    
    def _get_post_data(self, request: HttpRequest, selected_year: str) -> Dict[str, Any]:
        """ Fetch and process post data with cache magic """
        pinned, all_posts = self._get_filtered_posts(request.user, selected_year)
        
        # Add draft posts if user is authenticated
        if request.user.is_authenticated:
            draft_posts = Post.objects.filter(
                status=PostStatus.DRAFT.value,
                published__year=int(selected_year)
            ).select_related('author', 'category')
            all_posts = list(draft_posts) + list(all_posts)
        
        # Add summaries like adding sprinkles to cupcakes
        for post_list in [pinned, all_posts]:
            add_post_summaries(post_list)
            
        return {
            "pinned": pinned,
            "posts": all_posts,
            "years": self._get_cached_years(),
            "selected_year": selected_year,
        }
    
    def _get_user_data(self, request: HttpRequest) -> Dict[str, Any]:
        """👤 Get user data with a welcoming twist! 🎉"""
        return {"username": "Guest" if request.user.is_anonymous else request.user.username}
    
    def _get_activity_data(self, selected_year: str) -> Dict[str, Any]:
        """📊 Generate activity heatmap data with scientific precision 🔬"""
        year: int = int(selected_year)
        posts_queryset = Post.objects.all()
        weeks, max_count = get_activity_data(posts_queryset, year)
        return {"weeks": weeks, "max_count": max_count}
    
    def _get_selected_year(self, request: HttpRequest) -> str:
        """🗓️ Get selected year or current year as default ⏱️"""
        return request.GET.get("year") or str(timezone.now().year)
    
    def _get_cached_years(self) -> List[int]:
        """🧠 Cache years like a memorization champion 🏆"""
        # Clear cache to get fresh data
        cache.delete(self._POST_YEARS_CACHE_KEY)

        # Get fresh data
        if years := cache.get(self._POST_YEARS_CACHE_KEY):
            return years
        fresh_years = get_post_years()
        cache.set(self._POST_YEARS_CACHE_KEY, fresh_years, self._POST_YEARS_CACHE_TIMEOUT)
        return fresh_years
    
    def _get_filtered_posts(self, user: User, year: str) -> Tuple[List[Post], List[Post]]:
        """🔍 Filter posts with laser-sharp precision 🔦"""
        return get_filtered_posts(user, year)