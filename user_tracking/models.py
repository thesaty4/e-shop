from django.db import models
from django.db.models.deletion import CASCADE
from accounts.models import User
import datetime
# Create your models here.

# USER RECENT QUERY
class RecentQuery(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    query = models.CharField(max_length=200)
    query_date_time = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return "New Query at "+str(self.query_date_time)

# USER CLICK TRACK
class ClickCounter(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)
    overall_click = models.BigIntegerField()
    def __str__(self):
        return str(self.user)+" clicked "+str(self.overall_click)+" time"

####################################SPECIAL IMPORT#############################################
from selling_product.models import Category,Subcategory,Product
# ###############################################################################################

class ClickCategory(models.Model):                                              # 
    user = models.ForeignKey(User,on_delete=CASCADE)
    product_categories = models.ForeignKey(Category,on_delete=CASCADE)
    at_date_time = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):                                                                         #
        return str(self.user)+" clicked on "+str(self.product_categories)

class ClickSubcategory(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE)                         #
    product_subcategories = models.ForeignKey(Subcategory,on_delete=CASCADE)
    at_date_time = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return str(self.user)+' clicked on "'+str(self.product_subcategories)+'"'     #

class ClickProduct(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    product = models.ForeignKey(Product,on_delete=CASCADE)
    at_date_time = models.DateTimeField(default=datetime.datetime.now())                       #
    def __str__(self):
        return str(self.user)+" clicked on "+str(self.product)
#####################################END SPECIAL IMPORT##########################################

