from django.urls import reverse
from django.db import models
from ckeditor.fields import RichTextField
from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.
class Postnew(models.Model):
    postname = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    #description = models.TextField(blank=True)
    description = CKEditor5Field('Text', config_name='extends', blank=True)
    images = models.ImageField(upload_to='photos/products')
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('postnew_detail', args=[self.slug])

    def __str__(self):
        return self.postname