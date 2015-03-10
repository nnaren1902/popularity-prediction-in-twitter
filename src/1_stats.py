import common as common 
import config as config
import datetime,time
import json

for inputFile in config.input_file_list:
    with open(inputFile,'r') as inputFileObject:
        line = inputFileObject.readline();
        tweet = json.loads(line);
        startTime = common.getDateTime(tweet["tweet"]["created_at"]);
    #for each file, read the tweets 
    with open(inputFile,'r') as inputFileObject:
        count = 0;
        user_followers = 0;
        ##start from the first tweets time
    
        for line in inputFileObject:
            tweet = json.loads(line);      
           
            #now process each tweet  
            if (tweet != 0) and (type(tweet) is dict) :
                timeStamp = common.getDateTime(tweet["tweet"]["created_at"]);
                curTime = timeStamp;
                
                if(curTime <= (startTime+config.delta) ):
                        user_followers = user_followers + int(tweet['tweet']['user']['followers_count']);
                        count = count+1;
                     
                else:   
                                          
                    common.logAvgTweets(config.output_file_list[inputFile] , count, user_followers/count ,startTime, startTime+config.delta); 
                    startTime = startTime + config.delta; 
                    while  (curTime > (startTime+config.delta)) :
                           common.logAvgTweets(config.output_file_list[inputFile] , 0, 0, startTime, startTime+config.delta);
                           startTime = startTime+config.delta;
                           
                    
                    count =1;
                    user_followers = int(tweet['tweet']['user']['followers_count']);
        
        
    common.logAvgTweets(config.output_file_list[inputFile] , count , user_followers/count,startTime, startTime+config.delta);
       
        
    
    
        


    