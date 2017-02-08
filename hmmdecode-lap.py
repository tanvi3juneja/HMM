import sys
import re
import pickle
import math

inp=open('hmmmodel.txt','r')
transition_prob1=pickle.load(inp)
transition_prob={}
emission_prob={}
op=""
for keys,values in transition_prob1.items():
    if keys[0] in transition_prob:
        transition_prob[keys[0]][keys[1]]=values
    else:
        transition_prob[keys[0]]={}
        transition_prob[keys[0]][keys[1]]=values
emission_prob1=pickle.load(inp)
for keys,values in emission_prob1.items():
    if keys[0] in emission_prob:
        emission_prob[keys[0]][keys[1]]=values
    else:
        emission_prob[keys[0]]={}
        emission_prob[keys[0]][keys[1]]=values
tag_list=pickle.load(inp)
tagfreq=pickle.load(inp)
#print tag_list
arg=sys.argv[1]
#arg='C:/Users/tjune/Desktop/Spring 2016/NLP/hw6-dev-train/catalan_corpus_dev_raw.txt'
f=open(arg,'r')
temp=f.read()
line_file=temp.split('\n')
ppmatrix={}
backpointer={}
bstate=""
#print tag_list.__len__()
f2=open('hmmoutput.txt','w')
for line in line_file:
    w=line.split(" ")
    myfirstlist=[]
    if w[0] in emission_prob and emission_prob[w[0]].keys()>0:
        myfirstlist=emission_prob[w[0]].keys()
    else:
        myfirstlist=tag_list
    #     it2=float(emission_prob[w[0]].get((tag_list[s]), 0.0005))
    # myfirstlist=[]
    # if w[0] in emission_prob:
    #     myfirstlist=w[0]
    # else:
    #     myfirstlist=tag_list
    for s in myfirstlist:
        if w[0] in emission_prob:
            #it1=float(emission_prob[w[0]].get("Start",0.00005))
            it1 = float(emission_prob[w[0]].get(s, 1.0))
        else:
            it1=1.0
        ppmatrix[s,0]=float(it1*float(transition_prob["Start"].get(s,1.0/tagfreq[s])))
        backpointer[s,0]='Start'
    for t in range(1,w.__len__()):
        outr=[]
        inr=[]
        if w[t] in emission_prob:
            outr=emission_prob[w[t]].keys()
        else:
            outr=tag_list
        for i in outr:
            max=-1000000.0
            if w[t-1] in emission_prob and emission_prob[w[t-1]].keys()>0:
                inr=emission_prob[w[t-1]].keys()
            else:
                inr=tag_list
            if w[t] in emission_prob:
                it3=float(emission_prob[w[t]].get(i))
            else:
                it3=1.0
            bstate = ""
            for s in inr:
                #print ppmatrix.get((i,t),0.00005)

                c=0.0
                b=0.0
                a=float(ppmatrix.get((s, t - 1), 0.00005))
                if w[t] in emission_prob:
                    b=float(emission_prob[w[t]].get((i),1.0))
                else:
                    b=1.0
                if s in transition_prob:
                    c=float(transition_prob[s].get((i),1.0/tagfreq[s]))
                else:
                    c=1.0/tagfreq[s]
                d=a*b*c
                if max < d:
                    ppmatrix[i, t] = d
                    max = d
                    bstate=s
            backpointer[i,t]=bstate
    l=[]
    if w[w.__len__()-1] in emission_prob and emission_prob[w[w.__len__()-1]].keys()>0:
        l=emission_prob[w[w.__len__()-1]].keys()
    else:
        l=tag_list
    for tag in l:
        max=0.0
        it1=0.00005
        it2=0.00005

        if tag in transition_prob:
            it1=transition_prob[tag].get("End",1.0/tagfreq[tag])
        else:
            it1=1.0/tagfreq[tag]
        it2 =ppmatrix[tag,w.__len__()-1]
        f=it1*it2
        if f>max:
            max=f
            bstate=tag
    backpointer["End",w.__len__()]=tag
    #end state for backpointer
    j=w.__len__()
    fstate="End"
    loc=""
    while j>0:
        #print backpointer[fstate,j]
        #fstate2=backpointer[fstate,j]
        fstate1=(w[j-1])
        fstate=backpointer[fstate,j]
        loc=fstate1+"/"+fstate+" "+loc
        # max=-1000000.0
        # st=""
        # for x in range(0, tag_list.__len__()):
        #     if (float(ppmatrix.get((tag_list[x],j))>max)):
        #         max=float(ppmatrix.get((tag_list[x],j)))
        #         st=tag_list[x]
        # print st
        j=j-1
    if op=="":
        op=loc
    else:
        op=op+"\n"+loc
f2.write(op)
#print ppmatrix
#print time.clock()-start




