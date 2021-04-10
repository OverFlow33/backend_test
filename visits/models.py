from django.db import models
from django.contrib.auth.models import User

# Create the visit model in order to persist and manipulate the visitors information
class Visit(models.Model):
    # create a one to many relationship between the user the visit  
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # column represent the instant of the visit 
    created_at = models.DateTimeField('Date and time of the visit', auto_now_add=True)
    # considering that we are using ip v 4 so the format is XXX.XXX.XXX.XXX
    ip_address = models.CharField(max_length=15)

    # display the visit date and time instead of Object
    def __str__(self):
        return "visited at : " + str(self.created_at)

