from django.db import models

# Create your models here.
class MpesaTransaction(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    transaction_date = models.DateTimeField()

    def __str__(self):
        return f"{self.transaction_id} - {self.amount}"

