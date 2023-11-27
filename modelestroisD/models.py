from django.db import models
from django.utils import timezone
import uuid
import datetime
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.core.files import File

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Modele(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/', default='defaults/default_model_image.png')
    description = models.TextField()
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    timestamp = models.DateTimeField("Timestamp of creation", auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    
    def __str__(self):
        return self.name 
    
    def was_published_recently(self):
        return self.timestamp >= timezone.now() - datetime.timedelta(days=1)
    
    def get_latest_version_files(self):
        latest_version_files = []
        for variante in self.variantes.all():
            latest_version = variante.versions.last()
            if latest_version:
                latest_version_files.extend(latest_version.file.all())
        return latest_version_files
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  
        if self.image:
            img = Image.open(self.image)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            output_size = (400, 400)
            img = img.resize(output_size, Image.Resampling.LANCZOS)
            img.save(self.image.path)  

class Variante(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="images/", blank=True)
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE, related_name='variantes')
    tags = models.ManyToManyField(Tag, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return self.name 
    
    def was_published_recently(self):
        return self.timestamp >= timezone.now() - datetime.timedelta(days=1)
    
    def get_latest_version_files(self):
        latest_version = self.versions.last()
        if latest_version:
            return latest_version.file.all()
        return []
    
class Version(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    version_number = models.CharField(max_length=10, default="1.0")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images/", blank=True)
    variante = models.ForeignKey(Variante, on_delete=models.CASCADE, related_name="versions")
    tags = models.ManyToManyField(Tag, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="files/", blank=True)
    is_favorite = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
