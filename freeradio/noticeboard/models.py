from django.db import models
from django.dispatch import receiver
from django.conf import settings
from .settings import SIZES


class Notice(models.Model):
    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        editable=False
    )

    object_id = models.PositiveIntegerField(u'object ID', editable=False)
    subtitle = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    image_field = models.CharField(
        max_length=50,
        editable=False,
        null=True,
        blank=True
    )

    stickiness = models.PositiveIntegerField()
    cta_text = models.CharField(
        'call-to-action text',
        max_length=30,
        default=u'Find out more',
        null=True,
        blank=True
    )

    cta_url = models.CharField(
        'call-to-action URL',
        null=True,
        blank=True,
        max_length=255
    )

    added = models.DateTimeField()

    def __str__(self):
        return self.title

    @property
    def image(self):
        if not self.image_field:
            return None

        obj = self.content_type.get_object_for_this_type(pk=self.object_id)
        image_field = self.image_field.split('.')

        for part in image_field:
            obj = getattr(obj, part)

        return obj

    def get_blocks(self, media_size=1200):
        if not hasattr(self, '_blocks'):
            model = SIZES.get(
                '%s.%s' % (
                    self.content_type.app_label,
                    self.content_type.model
                ),
                {}
            )

            if media_size in model:
                self._blocks = model[media_size]
            else:
                self._blocks = model.get(
                    tuple(model.keys())[-1],
                    [1, 1]
                )

        return self._blocks

    @property
    def x_blocks(self):
        return self.get_blocks()[0]

    @property
    def y_blocks(self):
        return self.get_blocks()[1]

    class Meta:
        ordering = ('-added',)
        get_latest_by = 'added'


@receiver(models.signals.post_save)
def save_model(sender, instance, **kwargs):
    for (model, attrs) in getattr(settings, 'NOTICEBOARD_MODELS', ()):
        app_label, model = model.split('.')
        if instance._meta.app_label == app_label:
            if instance._meta.model_name.lower() == model.lower():
                from .helpers import add_or_update_notice

                add_or_update_notice(instance)
                return
