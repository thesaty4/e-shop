# ################# THIS ALGORITHEM WRITTEN BY SATYA NARAYAN MISHRA ###########
#   ALGORITHEMS -
#       [1] - NEW ARRIVAL PRODUCT SHOWN, ACCORDING USER INTREST FOR (LOGGED USER/ ANONYMOUS USER)
# #############################################################################
# NOW WE HAVE TO SHOW DATA TO USER BUT ONLY INTRESTED PRODUCT
# IN THE ARRIVAL PRODUCT SECTION, USER ABLE TO SEE LATEST PRODUCT ACCORDING HIS/HER INTREST
# [*] IF USER ARE LOGGEDIN - 
#     1- USERID REQUIRED
#     2- HOSTNAME OPTIONAL
#     3- HOST IP OPTIONAL
# -------------------------------
# [*] IF USER ARE ANONYMOUS - 
#     2- HOSTNAME REQUIRED
#     3- HOST IP REQUIED
# ===============================
# INTREST ANALYSIS ALGORITHM-
# 1 - BASED ON HIS/HER MAXIMUME VIEWS CATEGORY
# 2 - THOSE CATEGORY DATA SHOWING, WHAT THEY WATCH MOSTLY
# 3 - BASED ON TIMING, BEFORE 2 DAY WHAT DATA UPLOADED, WE FILTER FROM THERE
# 4 - IF PRODUCT HAVE LESS THAN 10 VIEWS THEN THOSE DATA WILL BE SHOWN
# =============================================================================

# from django.db.models.expressions import Random
from selling_product.models import ProductReview, Product,ProductUserViews,TotalViews,ProductViews,Category
from .auth import Calculation,time_day_ago
from django.db.models import Q
class Rating:
    def rating_avg(self,pid):
        pr = ProductReview.objects.filter(product=pid).count()
        if pr == 0:
            return 0
        else:
            star1 = ProductReview.objects.filter(product=pid,review_rating=1).count()
            star2 = ProductReview.objects.filter(product=pid,review_rating=2).count()
            star3 = ProductReview.objects.filter(product=pid,review_rating=3).count()
            star4 = ProductReview.objects.filter(product=pid,review_rating=4).count()
            star5 = ProductReview.objects.filter(product=pid,review_rating=5).count()
            # Avarage rating formula ar=1*star1+2*star2+3*star3+4*star4+5*star5/5
            AR=(1*star1+2*star2+3*star3+4*star4+5*star5)/(star1+star2+star3+star4+star5)
            return round(AR,1)

    def ratingCase(self,pid):
        try:totalViews = TotalViews.objects.get(product=pid)
        except TotalViews.DoesNotExist: totalViews = 0
        avgRating = self.rating_avg(pid)
        if totalViews == 0:
            return 'new'
        else:
            if avgRating == 0 and totalViews.views == 0:
                return 'new'
            elif avgRating == 0 and totalViews.views > 0:
                return 'new'
            elif avgRating <= 1 and totalViews.views <= 100:
                return 'd'
            elif avgRating <= 2 and totalViews.views <= 200:
                return 'c'
            elif avgRating <= 3 and totalViews.views <= 300:
                return 'b'
            elif avgRating <= 4 and totalViews.views <= 400:
                return 'a'
            elif avgRating <= 5 and totalViews.views <= 500:
                return 'a+'
            if (avgRating >= 4 and avgRating <= 5) and totalViews.views > 500:
                return 'a++'

class ArrivalProduct:
    categories = []
    categoryList = []
    # bestArrivalProducts=[]
    order_by=[]
    def __init__(self,sortBy):
        self.order_by.append(sortBy)
        self.categories.extend(list(Category.objects.all()))
        for d in self.categories:
            self.categoryList.append({d.id:0})   

    # LOGGDIN USER - MAIN METHOD
    def loggedUser(self,uid):
        # IF LOGIN USER REQUESTED 
        # print("is-authenticated")
        puvSet = ProductUserViews.objects.filter(user=uid)
        if puvSet.count() == 0:
            # IF DON'T HAVE ANY RECORD REGARDING LOGGED USER
            return self.defaultArrivalProduct()
        else:
            # IF WE HAVE RECORD REGARDING ANONYMOUS USER
            for viewer in puvSet:
                catId = viewer.product.category.id
                i=0
                for c in self.categories:
                    if catId in self.categoryList[i]:
                        self.categoryList[i][catId]+=1
                    i+=1

                # SORTING[{5: 0}, {6: 0}, {4: 1}, {1: 2}, {2: 7}, {5: 9}]
                # print(categoryList) #BEFORE SORTING
                calObj = Calculation(self.categoryList)
                sortedUserCategory = calObj.sortListDESC()

                categoryIds = []   # IN THIS LIST HAVE LATEST USER WATCHING PRODUCTS WITH SORTED DATA
                for x in sortedUserCategory:  
                    if list(x.values())[0] != 0:  # REMOVING ZERO VALUE
                        categoryIds.append(list(x.keys())[0])
                        # categoryIds.extend(x)

                # NEW LIST CREATION, IT HAVE ONLY WHAT USER WATCH EARLEAR AND PRODUCT ADDEDTIME BEFORE 2 DAYS OR UPLOADED LATEST, FOR LATEST PRODUCT
                filter_products =[]
                filter_products_id=[]
                for categoryId in categoryIds:
                    categoryProducts = Product.objects.filter(category=categoryId).order_by(self.order_by[0])
                    for catP in categoryProducts:
                        if catP.id not in filter_products_id:
                            filter_products_id.append(catP.id)
                            filter_products.append(catP)

                    # filter_products.extend(list(Product.objects.filter(category=categoryId).order_by('-id')[:5]))
                    # filter_products.extend(list(Product.objects.filter(Q(category=categoryId) | Q(add_date_time__gt=time_day_ago(2)))[:5]))

                # WE NEED SINGLE USER DATA SO, THAT'S WHY WE RETURN PRODUCT DURING RUNING LOOP 
                return self.getMoreProduct(filter_products)

    # ANONYMOUS USER - MAIN METHOD
    def anonymousUser(self,hostname,hostip):
         # IF ANONYMOUS USER REQUESTED 
        # print("is-authenticated")
        puvSet = ProductViews.objects.filter(host_name=hostname,host_ip=hostip)
        if puvSet.count() == 0:
            # IF DON'T HAVE ANY RECORD REGARDING ANONYMOUS USER
            return self.defaultArrivalProduct()
        else:
            # IF WE HAVE RECORD REGARDING ANONYMOUS USER
            for viewer in puvSet:
                catId = viewer.product.category.id
                i=0
                for c in self.categories:
                    if catId in self.categoryList[i]:
                        self.categoryList[i][catId]+=1
                    i+=1

                # SORTING[{5: 0}, {6: 0}, {4: 1}, {1: 2}, {2: 7}, {5: 9}]
                # print(categoryList) #BEFORE SORTING
                calObj = Calculation(self.categoryList)
                sortedUserCategory = calObj.sortListDESC()

                categoryIds = []   # IN THIS LIST HAVE LATEST USER WATCHING PRODUCTS WITH SORTED DATA
                for x in sortedUserCategory:  
                    if list(x.values())[0] != 0:  # FILTERING NOT ZERO VALUE
                        categoryIds.extend(x)

                # NEW LIST CREATION, IT HAVE ONLY WHAT USER WATCH EARLEAR AND PRODUCT ADDEDTIME BEFORE 2 DAYS, FOR LATEST PRODUCT
                filter_products =[]
                filter_products_id=[]
                for categoryId in categoryIds:
                    categoryProducts = Product.objects.filter(category=categoryId).order_by(self.order_by[0])
                    for catP in categoryProducts:
                        if catP.id not in filter_products_id:
                            filter_products_id.append(catP.id)
                            filter_products.append(catP)

                # filter_products.extend(list(Product.objects.filter(Q(category=categoryId) | Q(add_date_time__gt=time_day_ago(2)))[:5]))
                # WE NEED SINGLE USER DATA SO, THAT'S WHY WE RETURN PRODUCT DURING RUNING LOOP 
                return self.getMoreProduct(filter_products)

    
    def defaultArrivalProduct(self):
        # THIS FUNCTION RETURN THOSE PRODUCT WHO HAS UPLOADED RECENTALY AND GOOD RATING
        products=[]
        products.extend(list(Product.objects.all().order_by(self.order_by[0])))
        # products.extend(list(Product.objects.all().order_by(self.order_by[0])[:5]))
        return self.getMoreProduct(products)

    def getMoreProduct(self,filter_products):         
        bestSortProduct=[]
        def bestArrival(cs,fp,pd):
            if cs == 'new':
                bestSortProduct.insert(0,pd)
            elif cs == 'a++':
                bestSortProduct.insert(1,pd)
            elif cs == 'a+':
                bestSortProduct.insert(round(len(fp)/2),pd)
            elif cs == 'a':
                bestSortProduct.insert(round(len(fp)/3),pd)
            elif cs == 'b':
                bestSortProduct.insert(round(len(fp)/4),pd)
            elif cs == 'c':
                bestSortProduct.insert(round(len(fp)/5),pd)
            elif cs == 'd':
                bestSortProduct.insert(-1,pd)

        for p in filter_products:
            obj=Rating()
            # case = 'd'
            cases = obj.ratingCase(p.id)
            bestArrival(cases,filter_products,p)

        new_product=[]
        # IF PRODUCT VIEWS LESS THAN OR EQUAL 10 VIEWS
        total_views = TotalViews.objects.filter(views__lte=10).order_by("-id")
        for view in total_views:
            tvdata = Product.objects.filter(id=view.product.id) 
            new_product.extend(list(tvdata))

        secId = []
        for d in filter_products:
            secId.append(d.id)

        firId=[]
        for e in new_product:
            firId.append(e.id)

        # GET RATING OF PRODUCT
        obj=Rating()
        for ids in firId:
            if ids not in secId:
                pro=Product.objects.get(id=ids)
                # tvdata = Product.objects.filter(id=view.product.id) 
                cases = obj.ratingCase(ids)
                bestArrival(cases,filter_products,pro)
                # bestSortProduct.extend(list(Product.objects.filter(id=ids)))
        # self.bestArrivalProducts=bestSortProduct
        return bestSortProduct
    