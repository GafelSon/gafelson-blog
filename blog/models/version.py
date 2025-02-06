from django.db import models

class UpdateVersion(models.Model):
    version = models.CharField(max_length=10)
    date = models.DateField()
    
    class Meta:
        ordering = ['-date', '-version']

class UpdateFeature(models.Model):
    version = models.ForeignKey(UpdateVersion, related_name='features', on_delete=models.CASCADE)
    description = models.TextField()

class UpdateBugFix(models.Model):
    version = models.ForeignKey(UpdateVersion, related_name='bug_fixes', on_delete=models.CASCADE)
    description = models.TextField()