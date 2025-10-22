from django.db import models

# Create your models here.
class AnalyzedString(models.Model):
    id = models.CharField(max_length=64, primary_key=True) # sha256 hex
    value = models.TextField()
    properties = models.JSONField()
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['created_at'])]
        ordering = ['-created_at']

        def __str__(self):
            return f"{self.id} - {self.value[:40]}"