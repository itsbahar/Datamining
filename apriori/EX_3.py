import numpy as np
from collections import Counter
from itertools import combinations
import pandas as pd

def loadDataSet():
    data=pd.read_csv("games_sales_dataset.csv",header=None, low_memory=False)
    print(data.shape)
    data=data.values
    data_clean=[]
    for ar in data:
       data_clean.append(ar[~(pd.isna(ar))])
    return data_clean   


def build_matrix1(Sequences):
    item=[]
    for i in Sequences:
        item=list(set().union(item,i))
    
    i_c=len(item) 
    t_c=len(Sequences)
    
    matrix= np.zeros((t_c,i_c))
    for i in  range(len(Sequences)):
        for j in (Sequences[i]):
            index=item.index(j)
            matrix[i][index] = 1       
    return item , matrix

def gnrate_L1(matrix,min_sup):
    L1=Counter()
    #count item_set
    count=[]
    for i in range(matrix.shape[1]):
         count.append(int(np.sum(matrix[:,i])))
    
    for i in range(len(count)):
        if count[i] >= min_sup:
            L1[frozenset([i+1])] += count[i]       
    return L1

def findsubsets(s, n):
    temp=[]
    a=list(combinations(s, n))
    for i in a:
        temp.append(frozenset(i))
    return temp

#get list of set an cal superset
def super_set(sub_set):
    super_set=set({})
    for i in sub_set :
         super_set=super_set.union(i)
    return super_set    

def frequency(sub_set, matrix):
    c = Counter()
    for q in matrix:
        temp = np.where(q == 1)[0] + 1
        temp=set(temp)
        for i in sub_set:
             if (i).issubset(temp):
                    c[i] += 1
    return c

def subtract (l1,l2):
    return [x for x in l1 if x not in l2]

def make_join(lk,count):
    
    C1=list(lk)
    # print(C1)
    super_set=set({})
    for i in C1 :
         super_set=super_set.union(i)
    C=findsubsets(super_set,count)
    re=[]
    for c in C:
        sub=findsubsets(c,count - 1)
        flag=True
        for s in sub :
            if C1.count(s)==0:
                flag =False
                
        if flag == True:
            re.append(c)        
    return re   
   

def gnrate_L(L1,min_sup,matrix,item):
    encode = {1:item[0], 2:item[1], 3:item[2], 4:item[3], 5:item[4],6:item[5], 7:item[6], 8:item[7], 9:item[8], 10:item[9], 11:item[10], 12:item[11]} 
    count=2
    #C1
    C1=list(L1)
    Super_set=super_set(C1)
    C=findsubsets(Super_set, 2)
    L=[]
    Map=dict()
    while len(C) != 0:
        
          
        freq_item=frequency(C, matrix)
        lk = Counter()
        for i in freq_item:
            if(freq_item[i] >= min_sup):
        
                lk[i] += freq_item[i]
        f=open("frequent_itemset.txt", 'a')
        result="frequent_itemset"+'  '+str(count)+':'
        f.write(result)
        f.write("\n") 
        for j in lk:
            a=[]
            te=list(j)
            re_str="["
            for h in te:
               re_str=re_str+encode[h]+','
              
            re_str=re_str+']'
            
            f.write(re_str) 
            
            f.write("\n")                
        count +=1 
        if(len(lk) == 0):
            break 
        L.append(lk)
        Map.update(dict(lk))
        C=make_join(lk,count)
         
       
    Map.update(dict(L1))
    
    return L ,Map

def generate_rules(Map,L,min_conf,size_matrix,item):
    encode = {1:item[0], 2:item[1], 3:item[2], 4:item[3], 5:item[4],6:item[5], 7:item[6], 8:item[7], 9:item[8], 10:item[9], 11:item[10], 12:item[11]} 
    # encode = {1:item[0], 2:item[1], 3:item[2], 4:item[3], 5:item[4]}
    result = []
    
    for i in L:
        for lk in i:
            count=1
            while count != len(lk):
                sub_sets=findsubsets(lk,count)
                for k in sub_sets:
                    Right = subtract(lk,k)
                    Left = Map[frozenset(lk)]
                    sup =  Left/size_matrix
                    conf = Left / Map[frozenset(k)]
                    if conf >= min_conf:

                        Encode = []
                        for a in k :
                              Encode.append(encode[a])
                        left=[]    
                        for f in Encode:      
                              left.append(f)
                              
                        Encode = []
                        for a in Right :
                           Encode.append(encode[a])
                           
                        right=[]  
                        for f in Encode: 
                           right.append(f)
                           
                        
                        result.append([left,right, sup * 100,conf * 100])
                        
                count +=1        
    result.sort(key=lambda i:i[2])
    
    print(len(result))
    return result

def get_txtfile(result): 
    role_count=1
    with open("result.txt", "w") as f:
        for r in result:
            role = str(role_count)+':'+str(r[0])+'------>'+str(r[1])+' '+'Support : '+str(r[2])+" "+'Confidence :  '+str(r[3])
            f.write(role)
            f.write("\n")
            role_count +=1
                     
            
def recomment(role,item):
    count=0
    for i in item :
        print('number'+str(count)+":")
        print(i)
        count +=1
    print("if you want end type stop")    
    print('\n')
    
    client_buy =[]
    while True:
        product = input(" pleas select one number of item: \n" )
        if product == 'stop' :
            break 
        if int(product) < 12:
           client_buy.append(item[int(product)])
    
    print("select by client:")
    
    print(client_buy) 
    
    print(' New Game Recommendations :')  
       
    for r  in role:
        flag=True
        left=r[0]
        for g in left:
            if client_buy.count(g)==0 :
                  flag=False 
                         
        if (flag == True) and (len(client_buy) == len(left)):
            print((r[1]))
    
    
    
    
def apriori(min_sup,min_conf):
    transaction=loadDataSet()
    item , matrix = build_matrix1(transaction)
    min_sup = ((len(matrix) * min_sup)) / 100
    L1=gnrate_L1(matrix,min_sup)
    L,Map=gnrate_L(L1,min_sup ,matrix,item)
    role=generate_rules(Map,L,min_conf,len(matrix),item)
    
    get_txtfile(role)
    
    recomment(role,item)
####################################################main######################
apriori(0.1,0.5)