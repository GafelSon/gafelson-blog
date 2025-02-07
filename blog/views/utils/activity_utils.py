# views/utils/activity_utils.py
from collections import defaultdict
from datetime import timedelta
from django.utils import timezone
from typing import Tuple, List
from django.db.models.query import QuerySet

class ActivityVisualizer:
    """📊 Heatmap generator for post activity visualization"""
    
    @staticmethod
    def get_activity_data(posts: QuerySet, year: int = None) -> Tuple[List[List[dict]], int]:
        """🌋 Create volcanic activity map from post data"""
        post_counts = defaultdict(int)
        for post in posts.filter(published__year=year or timezone.now().year):
            post_counts[post.published.date()] += 1

        max_count = max(post_counts.values()) if post_counts else 0
        return ActivityVisualizer._build_weeks(post_counts, year), max_count

    @staticmethod
    def _build_weeks(post_counts: dict, year: int) -> List[List[dict]]:
        """🧱 Assemble weekly activity matrix with temporal alignment"""
        year = year or timezone.now().year
        start_date = timezone.datetime(year, 1, 1).date()
        weeks = []
        current_week = []
        
        # Calculate activity levels based on post counts
        max_count = max(post_counts.values()) if post_counts else 0
        
        # Add empty days to align with the start of week (Monday)
        start_weekday = start_date.weekday()  # Monday=0, Sunday=6
        if start_weekday > 0:
            for _ in range(start_weekday):
                current_week.append({'date': None, 'count': 0, 'activity_level': 0})
        
        # Fill in the days
        current_date = start_date
        while current_date.year == year:
            count = post_counts.get(current_date, 0)
            # Calculate activity level (0-3)
            if count == 0:
                activity_level = 0
            elif count <= max_count / 3:
                activity_level = 1
            elif count <= max_count * 2/3:
                activity_level = 2
            else:
                activity_level = 3
                
            day_data = {
                'date': current_date,
                'count': count,
                'activity_level': activity_level
            }
            
            current_week.append(day_data)
            
            # Start a new week after 7 days
            if len(current_week) == 7:
                weeks.append(current_week)
                current_week = []
            
            current_date += timedelta(days=1)
        
        # Add any remaining days and pad with empty days to complete the week
        if current_week:
            while len(current_week) < 7:
                current_week.append({'date': None, 'count': 0, 'activity_level': 0})
            weeks.append(current_week)
            
        return weeks