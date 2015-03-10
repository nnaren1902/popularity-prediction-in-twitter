import common as common 
import config as config
import datetime,time
import json
import sys

i =0;
with open(config.input_file_list[0],'r') as inputFile:
    for line in inputFile:
        
        tweet = json.loads(line);
        timeStamp = common.getDateTime(tweet["tweet"]["created_at"])
        curTime = int(time.mktime(timeStamp.timetuple()))
        post = tweet["tweet"]["created_at"];
        
        print str(timeStamp)+"\t"+post;