from rest_framework import serializers
from .models import UpdateVersion, UpdateFeature, UpdateBugFix

class UpdateVersionSerializer(serializers.ModelSerializer):
    features = serializers.StringRelatedField(source='features.values_list', read_only=True)
    bug_fixes = serializers.StringRelatedField(source='bug_fixes.values_list', read_only=True)

    class Meta:
        model = UpdateVersion
        fields = ['version', 'date', 'features', 'bug_fixes']