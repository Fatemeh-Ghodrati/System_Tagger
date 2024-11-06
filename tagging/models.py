from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Dataset(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
    
class Tag(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    dataset = models.ForeignKey(Dataset, related_name="tags", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def tagged_text_count(self):
        return self.texts.count()
    
    
class Text(models.Model):
    content = models.TextField()
    dataset = models.ForeignKey(Dataset, related_name="texts", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="texts")
    
    def __str__(self):
        return self.content[:50]
    
class OperatorAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=50)
