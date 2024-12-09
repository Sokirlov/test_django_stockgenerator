from django.db import models

class Currency(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="Full name of the currency (e.g., US Dollar).")
    iso_code = models.CharField(max_length=3, unique=True, help_text="ISO 4217 currency code (e.g., USD).")
    symbol = models.CharField(max_length=10, help_text="Symbol of the currency (e.g., $).")
    exchange_rate = models.FloatField(default=1.0, help_text="Exchange rate of the currency (e.g., $).")
    is_active = models.BooleanField(default=True, help_text="Whether the currency is currently available.")


    def __str__(self):
        return f"{self.iso_code}"
