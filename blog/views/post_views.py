from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpRequest
from django.utils.text import slugify
from typing import Dict, Any
import logging

from blog.models import Post, PostStatus
from datetime import datetime, timedelta
from collections import defaultdict

from .utils import calculate, words

logger = logging.getLogger(__name__)

class PostView(View):
    """🚀 Intergalactic post display with security shields and time mastery! ⏳🔒"""
    
    _DEFAULT_READING_TIME: str = "3 min"  # ⏱️ Fallback for time warp scenarios
    _REDIRECT_PERMANENT: bool = True      # 🔄 Permanent redirect flag
    
    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        """Handle GET requests with black hole-level error absorption 🌪️"""
        try:
            post = self._get_post(slug)
            self._check_canonical_redirect(slug, post)
            
            return render(
                request,
                'article.html',
                self._build_context(post)
            )

            response.headers.update(self._security_headers())
            
        except Post.DoesNotExist as e:
            logger.error(f"🚨 Post vanished from spacetime continuum: {slug}")
            raise Http404("Post does not exist") from e
            
        except Exception as e:
            logger.critical(f"🌋 Quantum flux detected in {slug}: {str(e)}")
            return render(request, '500.html', status=500)

    def _get_post(self, slug: str) -> Post:
        """🔍 Retrieve post with event horizon-level security (404 if escapes our reality)"""
        return get_object_or_404(Post.objects.all(), slug=slug)

    def _check_canonical_redirect(self, current_slug: str, post: Post) -> None:
        """🔄 Ensure we're using the official spacetime coordinates (slug)"""
        clean_slug = slugify(post.slug)
        if current_slug != clean_slug:
            raise RedirectException(post.get_absolute_url())

    def _build_context(self, post: Post) -> Dict[str, Any]:
        """🧱 Construct context fortress with multiple defense layers"""
        return {
            'post': post,
            'reading_time': self._get_reading_time(post.content),
            'words': self._get_word_count(post.content),
            'meta_tags': post.get_seo_meta(),
            'keywords': self._get_keywords(post.get_seo_meta().get('keywords', '')),
        }
    def _get_keywords(self, keywords_str: str) -> list:
        """📑 Process keywords into a clean list"""
        return [kw.strip() for kw in keywords_str.split(',') if kw.strip()]

    def _get_reading_time(self, content: str) -> str:
        """⏳ Calculate temporal requirements with quantum fallback"""
        return calculate(content) or self._DEFAULT_READING_TIME
    
    def _get_word_count(self, content: str) -> str:
         """ 🧮 Compute words count in article """
         return words(content) or "0"

    def _security_headers(self) -> Dict[str, str]:
        """🛡️ Force field headers to protect against dark web entities"""
        return {
            'X-Content-Type-Options': 'nosniff',
            'Strict-Transport-Security': 'max-age=63072000; includeSubDomains',
        }

class RedirectException(Exception):
    """🌀 Special exception for spacetime coordinate corrections"""
    def __init__(self, url: str):
        self.url = url
        super().__init__(f"Redirecting to canonical URL: {url}")