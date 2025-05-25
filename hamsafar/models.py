from django.db import models

class CompanionRequest(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    date = models.DateTimeField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.user.username} to {self.start_location} to {self.end_location} on {self.date}"  
    
    class Meta:
        db_table = 'companion_requests'
        managed = True
        verbose_name = 'Companion Request'
        verbose_name_plural = 'Companion Requests'
    
