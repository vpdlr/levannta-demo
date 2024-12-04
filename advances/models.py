from django.db import models
from django.utils.translation import gettext_lazy as _

class Portfolio(models.Model):
    avg_mrr = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    avg_churn_rate = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Portfolio (Avg MRR: {self.avg_mrr}, Avg Churn: {self.avg_churn_rate})"

class PortfolioMetrics(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="portfolio_metrics")
    year = models.IntegerField()
    month = models.IntegerField()
    mrr = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    churn_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.month}-{self.year} (MRR: {self.mrr}, Churn: {self.churn_rate})"

class Loan(models.Model):
    class LoanState(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')

    portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.CharField(max_length=10, choices=LoanState.choices, default=LoanState.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan {self.id} (State: {self.state}, Amount: {self.amount})"