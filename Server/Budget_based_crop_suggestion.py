import csv
predict={}
with open('data/cost-of-cultivation.csv') as csvfile:
    reader = csv.reader(csvfile)
    for x in reader:
    	predict[x[0]]=int(x[1])
def bestcrop(budget):
	rem=[]
	cos=[int(i) for x,i in predict.items()]
	for i in cos:
		if(i>budget):
			rem.append(-1)
		else:
			rem.append(cos)
	op={x:y for y,x in predict.items()}
	for i in rem:
		if(i!=-1):
			print(i)
			print(op[22810])

bestcrop(10000)