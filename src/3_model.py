import common as common 
import config as config
import time
import json

# Load modules and data
import numpy as np
import statsmodels.api as sm

np.random.seed(9876789)

#Increment count of tweets and corresponding retweets sum
def updateCount(tweet,tweetCount,retweetCount):
    return [tweetCount + 1,retweetCount + int(tweet['metrics']['citations']['total'])]

#Reset count of tweets and corresponding retweets sum
def resetCount(tweet):
    return [1,int(tweet['metrics']['citations']['total'])]


#determines if input square matrix (X) is positive definite - check before inverting
def isPD(X):
    return np.all(np.linalg.eigvals(X) > 0)

#write regression results to log file
def writeLog(fh,results):
    #params - parameters
    #bse - parameter std err
    #f_pvalue - Prob (F-statistic)
    #fvalue - F-statistic
    #mse_resid - sum of squared errors
    #pvalues - p values
    #resid - model residuals
    #rsquared - R-squared
    #tvalues - t values
    #conf_int(0.05) - 95% confidence intervals for each parameter (list of lists)
    #Predicted values: results.predict()
    for j in range(len(results.params)):
        fh.write(str(results.params[j])+'\t'+str(results.bse[j])+'\t'+str(results.tvalues[j])+'\t'+str(results.pvalues[j])+'\t'+str(results.conf_int(0.05)[j][0])+'\t'+str(results.conf_int(0.05)[j][1])+'\n')

    fh.write(str(results.f_pvalue)+'\t'+str(results.fvalue)+'\t'+str((results.mse_resid)/nTag)+'\t'+str(results.rsquared)+'\n')
    fh.write('\n')

#Number of hashtags to sweep
nTag = len(config.input_file_list)

#list that will track hashtag-specific features to regress on
#for each hashtag, there is a list of lists, where each list captures the following tuple
#   [curTweetHr, tweetCount, retweetCount, followerSum, followerMax, curDayHr, impCount, menSum, menMax, TagsSum, TagsMax]
#   curTweetHr - Unix-based hour
#   tweetCount - number of tweets with this hashtag posted during the hour
#   retweetCount - number of retweets of tweets with this hashtag posted during the hour
#   followerSum - sum of number of followers of tweet posters during the hour
#   followerMax - max of number of followers of tweet posters during the hour
#   curDayHr - {0-23}, representing time of day associated with curTweetHr
#   impCount - max of number of impressions of tweets with the hashtag during the hour
#   menSum - sum of number of mentions in tweets with the hashtag during the hour
#   menMax - max of number of mentions in tweets with the hashtag during the hour
#   TagsSum - sum of the number of other hashtags in the same tweet during the hour
#   TagsMax - max of the number of other hashtags in the same tweet during the hour
statList = [[[]] for x in range(nTag)]

for inputFile in config.input_file_list:
    print 'Processing ', inputFile
    #For each file, read the tweets
    firstTweet = True
    tweetCount = 0      #Tracks the number of original tweets including the hashtag in a given hour window
    retweetCount = 0    #Tracks the number of retweets including the hashtag in a given hour window
    followerSum = 0     #Tracks the sum of the number of followers of users who (re-)tweet the hashtag in a given hour window
    followerMax = 0     #Tracks the max of the number of followers of users who (re-)tweet the hashtag in a given hour window
    impCount = 0        #Tracks the max of the number of impressions of tweets including the hashtag in a given hour window
    menSum = 0        #Tracks the sum of the number of mentions in tweets including the hashtag in a given hour window
    menMax = 0        #Tracks the max of the number of mentions in tweets including the hashtag in a given hour window
    TagsSum = 0         #Tracks the sum of the number of other hashtags in tweets including the hashtag in a given hour window
    TagsMax = 0         #Tracks the max of the number of other hashtags in tweets including the hashtag in a given hour window
    with open(inputFile,'r') as inputFileObject:
        for line in inputFileObject:
            #Turn each file line into a JSON-based dictionary
            tweet = json.loads(line)
            #If the tweet is properly formatted:
            if (tweet != 0) and (type(tweet) is dict):
                #timeStamp will be used to generate UNIX time
                #dayHr is a number between 0-23 capturing hour of day (re-)tweet was published
                [timeStamp, dayHr] = common.getDateTime(tweet["tweet"]["created_at"])
                curTime = int(time.mktime(timeStamp.timetuple()))
                #tweetHr is the UNIX hour in which (re-)tweet was published
                tweetHr = curTime / 3600

                #######If this is the first sample in the file#######
                if firstTweet:
                    firstTweet = False
                    curTweetHr = tweetHr
                    curDayHr = dayHr

                    #Update count depending on whether this is a tweet or re-tweet
                    [tweetCount,retweetCount] = resetCount(tweet)

                    followerSum = int(tweet['original_author']['followers'])
                    followerMax = int(tweet['original_author']['followers'])

                    impCount = int(tweet['metrics']['impressions'])

                    menSum = int(len(tweet['tweet']['entities']['user_mentions']))
                    menMax = int(len(tweet['tweet']['entities']['user_mentions']))

                    TagsSum = int(len(tweet['tweet']['entities']['hashtags']) - 1)
                    TagsMax = int(len(tweet['tweet']['entities']['hashtags'])-1)
                #######If we find more (re-)tweets in this hour#######
                elif tweetHr == curTweetHr:

                    #Update count depending on whether this is a tweet or re-tweet
                    [tweetCount,retweetCount] = updateCount(tweet,tweetCount,retweetCount)

                    followerSum = followerSum + int(tweet['original_author']['followers'])
                    followerMax = max(followerMax,int(tweet['original_author']['followers']))

                    impCount = max(impCount, int(tweet['metrics']['impressions']))

                    menSum = menSum + int(len(tweet['tweet']['entities']['user_mentions']))
                    menMax = max(menMax, int(len(tweet['tweet']['entities']['user_mentions'])))

                    TagsSum = TagsSum + int(len(tweet['tweet']['entities']['hashtags']) - 1)
                    TagsMax = max(TagsMax, int(len(tweet['tweet']['entities']['hashtags'])-1))
                #######If it's time to move onto the next hour#######
                else:
                    statList[config.input_file_order[inputFile]].append([curTweetHr, tweetCount, retweetCount, followerSum, followerMax, curDayHr, impCount, menSum, menMax, TagsSum, TagsMax])

                    curTweetHr = tweetHr
                    curDayHr = dayHr

                    [tweetCount,retweetCount] = resetCount(tweet)

                    followerSum = int(tweet['original_author']['followers'])
                    followerMax = int(tweet['original_author']['followers'])

                    impCount = int(tweet['metrics']['impressions'])

                    menSum = int(len(tweet['tweet']['entities']['user_mentions']))
                    menMax = int(len(tweet['tweet']['entities']['user_mentions']))

                    TagsSum = int(len(tweet['tweet']['entities']['hashtags']) - 1)
                    TagsMax = int(len(tweet['tweet']['entities']['hashtags'])-1)
                    
    statList[config.input_file_order[inputFile]].append([curTweetHr, tweetCount, retweetCount, followerSum, followerMax, curDayHr, impCount, menSum, menMax, TagsSum, TagsMax])
    statList[config.input_file_order[inputFile]].remove([])


print 'Performing Day-to-Day Linear Regression'


# Notes on the Linear Regression Model
#   Output
#   1. Number of tweets during next day (tweets & retweets)
#   Regressors (from data in last 24 hour window)
#   1. Sum of the Number of tweets & their retweets
#   2. Maximum number of followers of those posting the hashtag
#   3. hour of day (0-23)
#   4. max of number of impressions of tweets with the hashtag during the hour
#   5. sum of number of mentions in tweets with the hashtag during the hour
#   6. max of number of mentions in tweets with the hashtag during the hour
#   7. sum of the number of other hashtags in the same tweet during the hour
#   8. max of the number of other hashtags in the same tweet during the hour

#Perform regression on a hour-to-hour rolling window over the range common to data from all hashtag JSON dumps
startHr = 394796
endHr = 395367

outputFH1 = open('log/part3_sweep_stats_OLS.txt','w')
outputFH2 = open('log/part3_sweep_stats_GLS.txt','w')

for i in range(startHr,endHr-46):
    print 'Processing Hr ', str(i+1-startHr), ' of ', str((endHr-46-startHr))
    #Need an intercept, so we add a column of 1's
    #X - array of data, row corresponds to data sample, and column corresponds to feature dimension (X = sm.add_constant(X))
    #y - functional output vector with same number of rows as X
    X = [[1,0,0,0,0,0,0,0,0] for a in range(nTag*24)]
    y = [0 for b in range(nTag*24)]

    #Extract the relevant data for next-hour prediction
    for j in range(nTag):
        for k in range(24):
            rec1 = [r for r in statList[j] if r[0] == (i+k)]
            rec2 = [r for r in statList[j] if r[0] == (i+24+k)]
            if rec1 != []:
                X[j*24 + k][1] = rec1[0][1] + rec1[0][2]    #sum of tweets and their retweets
                X[j*24 + k][2:9] = rec1[0][4:11]
            if rec2 != []:
                y[j*24 + k] = rec2[0][1]

    #OLS - ordinary LS: errors are iid
    #Fit & save statistical information
    model = sm.OLS(y, X)
    results = model.fit()

    writeLog(outputFH1,results)

    #GLS - generalized LS: errors are independent but heteroscedastic (different variance)
    #Fit & save statistical information
    residVar = np.diag([a**2 for a in results.resid])
    #round the values of the residual covariance matrix to avoid inversion of singular matrices
    residVar = [[round(a2,4) for a2 in a1] for a1 in residVar]
    #can perform GLS if the residual covariance matrix is invertible
    if isPD(residVar):
        model = sm.GLS(y, X, residVar)
        results = model.fit()

    writeLog(outputFH2,results)


outputFH1.close()
outputFH2.close()
