from django.db import models

class ScrapeJob(models.Model):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
    ]
    
    site_name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    run_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.site_name} - {self.status} - {self.run_at}"
