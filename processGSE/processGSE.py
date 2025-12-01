import numpy as np
import math
import random
import pandas as pd 

GSEseries=input("file?")

data = pd.read_csv(GSEseries+'_series_matrix.txt', comment='!', sep='\t',index_col=0)

#print(list(data.columns))
#print(list(data.index))

pd.DataFrame(data.values).to_csv("./data.csv", header=None, index =None)
pd.DataFrame(list(data.index)).to_csv("./features_0.csv", header=None, index =None)
pd.DataFrame(list(data.columns)).to_csv("./ids.csv", header=None, index =None)


pd.DataFrame(np.transpose(data.values)).to_csv("./dataT.csv", header=None, index =None)

# Using readlines()
file1 = open(GSEseries+'_series_matrix.txt', 'r', encoding="utf8" )
Lines = file1.readlines()
 
templabels=[]
count = 0
# Strips the newline character
for line in Lines:
	if "Sample_characteristics_ch1" in line:
		line=line.replace('"','')
		line=line.replace('\n','')
		lineVector=line.split('\t')
		templabels.append(lineVector)
		
print(templabels)	

pd.DataFrame(np.array(templabels)).T.to_csv("./templabels.csv", header=None, index =None)