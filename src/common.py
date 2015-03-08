def readTweets(inputFile):
    with open(inputFile,'r') as inputFileObject:
        for line in inputFile:
            tweetObject = json.loads(line);        
            if (tweetObject != 0) and (type(tweetObject) is dict) :
    #             numberOfRetweetsForCurrentTweet = tweetObject["tweet"]["retweet_count"]
               