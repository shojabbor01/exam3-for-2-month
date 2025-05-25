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
    

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'users'
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
class Trip(models.Model):
    user = models.ForeignKey(User, related_name='trip_related', on_delete=models.CASCADE)
    start_location = models.CharField(max_length=50)
    end_location = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)
    seats_available = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"trip user {self.user}"
    
    class Meta:
        db_table = 'trips'
        managed = True
        verbose_name = 'Trip'
        verbose_name_plural = 'Trips'
