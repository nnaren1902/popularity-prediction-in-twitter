import common as common 
import config as config
import datetime,time
import json

for inputFile in config.input_file_list:
    #for each file, read the tweets 
    with open(inputFile,'r') as inputFileObject:
        count = 0;
        user_followers = 0;
        for line in inputFileObject:
            tweet = json.loads(line);      
           
            #now process each tweet  
            if (tweet != 0) and (type(tweet) is dict) :
                timeStamp = common.getDateTime(tweet["tweet"]["created_at"])
                curTime = int(time.mktime(timeStamp.timetuple()))
                
                user_followers = user_followers + int(tweet['tweet']['user']['followers_count'])
                count = count+1;
                 
                if count == 1:
                    startTime = timeStamp;
                    minTime = int(time.mktime(startTime.timetuple()));
                    
        delta = (curTime - minTime)/3600;
       
        common.logAvgTweets(config.output_file_list[inputFile] , count/delta , user_followers/count);
    
    
        


    