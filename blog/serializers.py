from rest_framework import serializers
from .models import Post, UpdateVersion, UpdateFeature, UpdateBugFix


class UpdateVersionSerializer(serializers.ModelSerializer):
    features = serializers.StringRelatedField(source='features.values_list', read_only=True)
    bug_fixes = serializers.StringRelatedField(source='bug_fixes.values_list', read_only=True)

    class Meta:
        model = UpdateVersion
        fields = ['version', 'date', 'features', 'bug_fixes']

class PostCreateSerializer(serializers.ModelSerializer):
    duplicate_count = serializers.IntegerField(write_only=True, required=False, default=1)
    target_date = serializers.DateField(write_only=True, required=True)
    
    class Meta:
        model = Post
        fields = ['title', 'content', "subtitle", 'category', "status", 'slug', 'author', 'duplicate_count', 'target_date']
        
    def validate_duplicate_count(self, value):
        if value < 1 or value > 50:
            raise serializers.ValidationError("Duplicate count must be between 1 and 50")
        return value