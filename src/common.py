import json
import datetime

class CaseInsensitiveDict(dict):
    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(key.lower())
    
    
month_dict = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12};

def logBinTweets(outputFile , average ,startTime, endTime,mode='a'):
    with open(outputFile,mode) as outputFileObject:
        to_write ="startTime :"+str(startTime)+" || endTime :"+str(endTime)+ " || tweets/hour :"+ str(average)+"\n";
        outputFileObject.write(to_write);  
        print ("done"); 


def logAvgTweets(outputFile, avg_tweets_per_hour , avg_followers , avg_retweet):
    with open(outputFile,'w') as outputFileObject:
        to_write = "average tweets/hour :"+str(avg_tweets_per_hour)+"|| average follower count : "+str(avg_followers)+"|| average retweet count : "+str(avg_retweet)+"\n";
        outputFileObject.write(to_write);
        print ("done logging averages");
        
def getDateTime(strTime):
    list = strTime.split(" ");
    time_str = list[3].split(":");
   
    dateObject = datetime.datetime(int(list[5]),month_dict[list[1]] , int(list[2]), int(time_str[0]), int(time_str[1]), int(time_str[2]) );
    return dateObject;
    