import sys
import re
import pickle
import math
f1=sys.argv[1]
#f1='C:/Users/tjune/Desktop/Spring 2016/NLP/hw6-dev-train/catalan_corpus_train_tagged.txt'
f=open(f1,'r')
temp=f.read()
w=temp.split("\n")
wtm={}
TagCount={}
TTCount={}
p1={}
p2={}
counter=0
tag_list=list()
postagfreq={}
for line in w:
    counter+=1
    t=line.split(" ")
    ptag="Start"
    for wod in t:
        x=wod.split("/")
        if len(x)==2:
            (word,tag)=x
            if tag not in tag_list:
                tag_list.append(tag)
            postagfreq[tag]=postagfreq.get(tag,0.0)+1.0
            wtm[word,tag]=wtm.get((word,tag),0)+1
            TagCount[tag]=TagCount.get(tag,0) + 1
            TTCount[ptag,tag]=TTCount.get((ptag,tag),0) + 1
            ptag=tag
    ftag='End'
    TTCount[tag,ftag]=TTCount.get((tag,ftag),0) + 1
TagCount['Start']=counter
TagCount['End']=counter
for key, val in TTCount.items():
    val1=TagCount.get(key[0])
    p1[key]=float(val)/float(val1)
#print p1
for key, val in wtm.items():
    val2=TagCount.get(key[1])
    p2[key]=float(val)/float(val2)
#print p1
f2=open('hmmmodel.txt','wb')
pickle.dump(p1,f2)
pickle.dump(p2,f2)
pickle.dump(tag_list,f2)
pickle.dump(postagfreq,f2)
f2.close()
