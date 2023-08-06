from parler.admin import TranslatableAdmin


class BaseAdmin(TranslatableAdmin):  # base class should subclass 'django.db.models.Model'
    list_display = ['id',
                    'slug',
                    'publish',
                    'created',
                    'updated',
                    'status']
    list_filter = ['id',
                   'slug',
                   'publish',
                   'created',
                   'updated',
                   'status']
    list_editable = ['status']

    class Meta:
        abstract = True  # Set this model as Abstract
        ordering = ('slug',)

        def __str__(self):
            return self.slug

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
