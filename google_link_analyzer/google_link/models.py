from django.db import models

# Create your models here.

class google_link_analyzer(models.Model):  
    
    link_id = models.AutoField(primary_key=True)
    search_key =models.CharField(max_length=90)
    user = models.CharField(max_length=90)
    status =models.CharField(max_length=90)
    details = models.TextField()
    web_link = models.CharField(max_length=350)
   
    timestamp = models.DateTimeField(null=False)


    class Meta:
        db_table = 'google_link_analyzer'
