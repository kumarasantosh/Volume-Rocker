from django.db import models

# Create your models here.


class NseDataCoi(models.Model):
    strikePrice = models.IntegerField()
    underlying = models.CharField(max_length=250)
    changeinOpenInterestPE = models.DecimalField(
        max_digits=50, decimal_places=0)
    changeinOpenInterestCE = models.DecimalField(
        max_digits=50, decimal_places=0)
    Diffrence = models.DecimalField(max_digits=20, decimal_places=0)
    SpotPrice = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.strikePrice}"
