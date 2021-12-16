from datetime import timedelta
from django.utils import timezone
def time_day_ago(before):
    return timezone.now() - timedelta(days=before)

def dataValidate(data):
    dangerText = "</\!`~{>"
    i=0
    freshData = ""
    for singleChar in data:
        if singleChar not in dangerText:
            freshData += singleChar
    return freshData.strip()

class Calculation:
    datas = []
    def __init__(self,data):
        self.datas=data

    def maxList(self):
        maxNum=0
        max=self.datas[0]
        for data in self.datas:
            if maxNum < list(data.values())[0]:
                maxNum=list(data.values())[0]
                max=data
        return max
                
    def minList(self):
        minNum=0
        min=self.datas[0]
        for data in self.datas:
            if minNum > list(data.values())[0]:
                minNum=list(data.values())[0]
                min=data
        return min

    def sortListASC(self):
        tempDict=[]
        for pre in range(len(self.datas)):
            for post in range(len(self.datas)):
                if list(self.datas[pre].values())[0] < list(self.datas[post].values())[0]:
                    tempDict=self.datas[post]
                    self.datas[post]=self.datas[pre]
                    self.datas[pre]=tempDict
        return self.datas

    def sortListDESC(self):
        tempDict=[]
        for pre in range(len(self.datas)):
            for post in range(len(self.datas)):
                if list(self.datas[pre].values())[0] > list(self.datas[post].values())[0]:
                    tempDict=self.datas[post]
                    self.datas[post]=self.datas[pre]
                    self.datas[pre]=tempDict
        return self.datas

    def sortASC(self):
        temp=0
        for i in range(len(self.datas[0])):
            for j in range(len(self.datas[0])):
                if(self.datas[0][i] < self.datas[0][j]):
                    temp=self.datas[0][i]
                    self.datas[0][i]=self.datas[0][j]
                    self.datas[0][j]=temp
        return self.datas[0]

    def sortDESC(self):
        temp=0
        for i in range(len(self.datas[0])):
            for j in range(len(self.datas[0])):
                if(self.datas[0][i] > self.datas[0][j]):
                    temp=self.datas[0][i]
                    self.datas[0][i]=self.datas[0][j]
                    self.datas[0][j]=temp
        return self.datas[0]

    def max(self):
        max=self.datas[0][0]
        for data in self.datas[0]:
            if max < data:
                max=data
        return max

    def min(self):
        min=self.datas[0][0]
        for data in self.datas[0]:
            if min > data:
                min=data
        return min

    def avg(self):
        count = 1
        total=0
        sum=0
        for data in self.datas[0]:
            sum+=data*count
            total+=data
            count+=1
        return round(total/sum,2)

