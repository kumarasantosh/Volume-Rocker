from django.db import models

# Create your models here.


my_choises = (
    ("PE", "PE"),
    ("CE", "CE")
)


class NSE_DATA(models.Model):
    name = models.CharField(max_length=250, choices=my_choises)
    underlying = models.CharField(max_length=250)
    strikePrice = models.DecimalField(max_digits=50, decimal_places=0)
    expiryDate = models.DateField(blank=True, null=True)
    openInterest = models.DecimalField(max_digits=50, decimal_places=0)
    changeinOpenInterest = models.DecimalField(max_digits=50, decimal_places=0)
    totalTradedVolume = models.DecimalField(max_digits=50, decimal_places=0)
    underlyingValue = models.DecimalField(max_digits=50, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.underlying} - {self.strikePrice}"
