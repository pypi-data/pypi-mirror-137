from django.utils import timezone
from django.db import models


class Base(models.Model):  # base class should subclass 'django.db.models.Model'
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    slug = models.SlugField(max_length=250,
                            db_index=True,
                            unique=True,)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              db_index=True,
                              choices=STATUS_CHOICES,
                              default='draft')

    class Meta:
        abstract = True  # Set this model as Abstract
        ordering = ('slug',)

        def __str__(self):
            return self.slug

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
