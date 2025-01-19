from django.db import models


# Create your models here.

def generate_id():
    import uuid
    key = uuid.uuid4().hex[:10]
    while True:
        if Payment.objects.filter(id=key).exists():
            key = uuid.uuid4().hex[:10]
        else:
            break
    return key


class Payment(models.Model):
    id = models.CharField(max_length=10, primary_key=True, unique=True, default=generate_id)
    amount = models.CharField(max_length=10)
    currency = models.CharField(max_length=10)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default="pending", choices=(("pending", "pending"), ("success", "success"),
                                                                         ("failed", "failed")))
    category = models.CharField(max_length=100, default="")
    razorpay_order_id = models.CharField(max_length=255, default="asdf")

    def __str__(self):
        return self.id
