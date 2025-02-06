from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Speaker

@receiver(pre_delete, sender=Speaker)
def reorder_speakers(sender, instance, **kwargs):
    speakers_gt_order = Speaker.objects.filter(order__gt=instance.order)
    for speaker in speakers_gt_order:
        speaker.order -= 1
        speaker.save()
