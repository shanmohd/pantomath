from django.shortcuts import render
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
import os
import requests
import tweepy
from textblob import TextBlob


def twitterHero(data,size):

    consumer_key='FQjveS1W4XQd9tWir6BwpdUcI'
    consumer_secret='Cnj2ATLmzMoCXg2HlHtvB9tpLujO6WmlESDeTQhaiyqqFwgrbH'
    access_token= '3224526254-mjY3zRNPpQOEP3VxTlU1eaviBWyrXme12VB7Hli'
    access_token_secret='yKzfDd1lFVWZnZnm3nQjSipOLRqn93MWoyDAobN3C1iJN'

    auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)

    api=tweepy.API(auth, wait_on_rate_limit=True)
    S=[]
    counter=[0,0,0] 
    for tweet in tweepy.Cursor(api.search, q=data, lang="en").items(size):
        analysis=TextBlob(tweet.text)
        if analysis.sentiment.polarity > 0:
            res='positive'
            counter[0]+=1
        elif analysis.sentiment.polarity == 0:
            res='neutral'
            counter[2]+=1
        else:
            res='negative'
            counter[1]+=1
        S.append((tweet.text,analysis.sentiment,res))

    positivePer=(counter[0]/size)*100
    negativePer=(counter[1]/size)*100
    neutralPer=(counter[2]/size)*100
    S.append((positivePer,negativePer,neutralPer))
    return S


def index(request):
    return render(request,'website/home.html',{})


def form_data(request):
    try:
        data=request.POST['q']
        size=int(request.POST['size'])
    except MultiValueDictKeyError:
        data='data science'
        size=50
    if data=='':
        data='data science'
    S=twitterHero(data,size)
    posPer,negPer,ntrPer=S[-1][0],S[-1][1],S[-1][2]
    del S[-1]
    return render(request,'website/index.html',{'data':S,'size':size,'search':data,'posPer':posPer,'negPer':negPer,'ntrPer':ntrPer})
