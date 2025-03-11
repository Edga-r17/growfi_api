from django.db import models
from _base.models import BaseModel
from django.utils.timezone import now
from datetime import timedelta
from users.models import GrowfiUser 

class Transaction(BaseModel):
    user = models.ForeignKey(GrowfiUser, on_delete=models.CASCADE, related_name="transactions",verbose_name="Usuario")
    date = models.DateField('Fecha',blank=True, null=True)
    amount = models.DecimalField('Monto', max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.CharField('Categoria', max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user_id} - {self.date} - {self.amount} - {self.category}"
    
    @staticmethod
    def last_30_days_transactions(user_id):
        return Transaction.objects.filter(
            user_id=user_id,
            date__gte=now().date() - timedelta(days=30)
        ).values("category").annotate(total=models.Sum("amount"))

