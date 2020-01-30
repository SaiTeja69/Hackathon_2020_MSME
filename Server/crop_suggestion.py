from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import csv
import datetime
import sys
import os
import pandas as pd
present=datetime.datetime.now()
month=present.month
location='Hyderabad'
state="Telangana"
temp=[]
temp_final=[]
rain_fall=[]
rainfall_final=[]
prevtemp=0
prevrainfall=0
def conv(nutrient):
    nutrient_dict={'VL':1,'L':2,'M':3,'H':4,'VH':5 }
    return  nutrient_dict.__getitem__(nutrient)
with open('data/temprainfall.csv') as csvfile:
    reader = csv.reader(csvfile)
    count=0
    for row in reader:
        if(count<13):
           temperature=(float(row[3])+float(row[4]))/2
           temp.append(round(temperature,2))
           rain_fall.append(float(row[5]))
           count=count+1
def rainfall(temp_final,rainfall_final,temp,rain_fall):    
    index=month-1
    prevtemp=0
    prevrainfall=0    
    for i in range (1,13):
        prevtemp=prevtemp+temp[index]
        temp_final.append(round((prevtemp/i),2))
        prevrainfall=prevrainfall+rain_fall[index]
        rainfall_final.append(round(prevrainfall,2))
        index= index+1
        if index==12:
            index=0
def nutrients(state,rainfall_final,temp_final):
    try:
        with open('data/nutrientsarea.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
               count=0
               if(count<1):
                   narea=conv(row[1])
                   parea=conv(row[2])
                   karea=conv(row[3])
                   ph=row[4]
                   count=count+1
    except IOError:
       sys.exit("The required file does not exist!!!")               
    csvfile.close
    try:
        
        with open('data/cropDB.csv', 'r') as csvfile, open('data/metacrops.csv', 'w') as metacrops:
            reader = csv.reader(csvfile)
            metacrops.writelines("Crop, Rainfall, Temperature, pH \n")
            for row in reader:
               ncrop=conv(row[8])
               pcrop=conv(row[9])
               kcrop=conv(row[10])
               if(narea>=ncrop and parea>=pcrop and karea>=kcrop):
                   no_months=int(row[1])
                   total=row[0]+","+str(rainfall_final[no_months-1])+","+str(temp_final[no_months-1])+","+ph+"\n"
                   metacrops.writelines(total)
    except IOError:
       sys.exit("The required file does not exist!!!")     
    csvfile.close
    metacrops.close 
def filewrite():
    n=1
    try:
        with open("data/metacrops.csv",'r') as f:
            with open("data/metacrops11.csv", "w") as f1:
                for line in f:
                    if n==1:
                        n=n+1
                        continue
                    f1.write(line)
    except IOError as e:
            sys.exit("No such file exists")
    f.close
    f1.close  

def regression(): 
    n=0
    crop_Y_pred=[]
    crop_name=[]
    dataset=pd.read_csv('data/regressiondb.csv')
    locbased=pd.read_csv('data/metacrops.csv')  
    try:
       with open('data/metacrops11.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
               crop=row[0]
               metadata=dataset.loc[dataset['Crop'] == crop]
               X = metadata.iloc[:, :-2].values
               Y = metadata.iloc[:, 4].values
               X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.1, random_state = 0)
               regressor = LinearRegression()
               regressor.fit(X_train, Y_train)  
               X_locbased = locbased.loc[[n]].values
               X_locbased = X_locbased[:, 1:4]
               Y_pred=regressor.predict(X_locbased)
               if Y_pred>0:
                   crop_Y_pred.append(round(Y_pred[0],3))
                   crop_name.append(crop)
       sorted_crops=quicksort(crop_name,crop_Y_pred,0,len(crop_Y_pred)-1)                       
       csvfile.close
       return sorted_crops
   
    except IOError:
        sys.exit("No such file exists")                 
def quicksort(crop_name,crop_Y_pred,start, end):
    if start < end:
        pivot = partition(crop_name,crop_Y_pred, start, end)
        quicksort(crop_name,crop_Y_pred, start, pivot-1)
        quicksort(crop_name,crop_Y_pred, pivot+1, end)
    return crop_name
def partition(crop_name,crop_Y_pred, start, end):
    pivot = crop_Y_pred[start]
    left = start+1
    right = end
    done = False
    while not done:
        while left <= right and crop_Y_pred[left] >= pivot:
            left = left + 1
        while crop_Y_pred[right] <= pivot and right >=left:
            right = right -1
        if right < left:
            done= True
        else:
            temp=crop_Y_pred[left]
            crop_Y_pred[left]=crop_Y_pred[right]
            crop_Y_pred[right]=temp
            temp1=crop_name[left]
            crop_name[left]=crop_name[right]
            crop_name[right]=temp1
    temp=crop_Y_pred[start]
    crop_Y_pred[start]=crop_Y_pred[right]
    crop_Y_pred[right]=temp 
    temp1=crop_name[start]
    crop_name[start]=crop_name[right]
    crop_name[right]=temp1
        
    return right    
def ListtoStr(sorted_crop):
    pred_crop = ""
    comma_flag=0
    no=len(sorted_crop)
    if(no>10):
        no=10
    for i in range (no):
        if comma_flag==1:
            pred_crop=pred_crop+","
                       
        pred_crop= pred_crop + sorted_crop[i]
        comma_flag=1
    return pred_crop
if __name__ == '__main__':

    rainfall(temp_final,rainfall_final,temp,rain_fall)
    nutrients(state,rainfall_final,temp_final)
    filewrite()
    sorted_crop=regression()
    final_crop=ListtoStr(sorted_crop)
    print (final_crop)