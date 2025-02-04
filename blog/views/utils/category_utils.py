# views/utils/category_utils.py
from django.shortcuts import get_object_or_404
from django.http import HttpRequest, HttpResponse
from blog.models import Category, Post

class CategoryHandler:
    """📂 Taxonomic content organizer with SEO optimization modules"""
    
    @staticmethod
    def get_category_context(slug: str) -> dict:
        """🔍 Category data miner with error suppression field"""
        category = get_object_or_404(Category, slug=slug)
        return {
            'category': category,
            'posts': category.posts.filter(status=Post.PostStatus.PUBLISHED.value),
            'meta_tags': category.get_seo_meta()
        }