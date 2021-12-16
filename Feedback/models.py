from django.db import models
from django.db.models.deletion import CASCADE
# from django.contrib.auth.models import User
from accounts.models import User
from EshopApp.models import SiteInfo
# Create your models here.
class UserFeedback(models.Model):
    site = models.ForeignKey(SiteInfo,on_delete=CASCADE)
    user = models.ForeignKey(User,on_delete=CASCADE)
    name = models.CharField(max_length=50,help_text="Notic: This name will show publicaly")
    feedback = models.TextField(max_length=500)

    def __str__(self):
        return str(self.site)+" : "+self.name+" - Feedback"