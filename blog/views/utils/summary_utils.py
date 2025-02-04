# views/utils/summary_utils.py
from typing import Optional
from django.db.models import QuerySet
from blog.models import Post

class PostSummarizer:
    """ Content distillation expert with smart truncation algorithms ✂️"""
    
    _DEFAULT_SUMMARY = "Count yourself!"  # Fallback for mystery content
    
    @classmethod
    def summarize(cls, post: Post, max_length: int = 80) -> str:
        """ Extract first sentence summary with length protection """
        if not post.content:
            return cls._DEFAULT_SUMMARY
            
        sentences = post.content.split('.')
        first_sentence = (sentences[0].strip() + '.' if sentences else '')[:max_length]
        return f"{first_sentence}..." if len(first_sentence) == max_length else first_sentence

    @classmethod
    def add_post_summaries(cls, posts: QuerySet[Post]) -> None:
        """ Batch-process summaries like a content ninja """
        for post in posts:
            post.summary = cls.summarize(post)