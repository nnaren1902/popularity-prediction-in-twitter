import common as common 
import config as config
import datetime,time
import json

for inputFile in config.input_file_list:
    with open(inputFile,'r') as inputFileObject:
        line = inputFileObject.readline();
        tweet = json.loads(line);
        startTime = common.getDateTime(tweet["tweet"]["created_at"]);
        
        overall_start_time = startTime;
    #for each file, read the tweets 
    with open(inputFile,'r') as inputFileObject:
        total_count = 0;
        total_user_followers = 0;
        total_retweet = 0;
        count = 0;
        
    
        
        ##start from the first tweets time
    
        for line in inputFileObject:
            tweet = json.loads(line);      
           
            #now process each tweet  
            if (tweet != 0) and (type(tweet) is dict) :
                timeStamp = common.getDateTime(tweet["tweet"]["created_at"]);
                curTime = timeStamp;
                overall_end_time = timeStamp;
                
                total_count = total_count +1;
                total_user_followers = total_user_followers + int(tweet['tweet']['user']['followers_count']);
                total_retweet = total_retweet + int(tweet['metrics']['citations']['total']);
                
                if(curTime <= (startTime+config.delta) ):
                        count = count+1;
                        
                     
                else:   
                                          
                    common.logBinTweets(config.output_file_list1[inputFile] , count ,startTime, startTime+config.delta); 
                    
                    startTime = startTime + config.delta; 
                    while  (curTime > (startTime+config.delta)) :
                           common.logBinTweets(config.output_file_list1[inputFile] , 0, startTime, startTime+config.delta);
                           startTime = startTime+config.delta;
                           
                    
                    count =1;
                    
        
        
    common.logBinTweets(config.output_file_list1[inputFile] , count ,startTime, startTime+config.delta);
    
    #log the averages
    timeDelta = overall_end_time - overall_start_time;
    
    timeDelta_hours = timeDelta.total_seconds()/3600;
    
    common.logAvgTweets(config.output_file_list2[inputFile] , total_count/timeDelta_hours , total_user_followers/total_count , total_retweet/total_count);
       
        
    
    
        


    