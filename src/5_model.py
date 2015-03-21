import common as common
import config as config
import time
import json

# Load modules and data
import numpy as np
import statsmodels.api as sm

from sklearn import cross_validation

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

# get the test data attributes
def getTestData(inputFile):
    testList = [[]]
    firstHour=1000000
    lastHour=-1
    print 'Processing ', inputFile
    firstTweet = True
    tweetCount = 0      #Tracks the number of original tweets including the hashtag in a given hour window
    retweetCount = 0    #Tracks the number of retweets including the hashtag in a given hour window
    followerSum = 0     #Tracks the sum of the number of followers of users who (re-)tweet the hashtag in a given hour window
    followerMax = 0     #Tracks the max of the number of followers of users who (re-)tweet the hashtag in a given hour window
    impCount = 0        #Tracks the max of the number of impressions of tweets including the hashtag in a given hour window
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

                if(tweetHr>lastHour):
                    lastHour = tweetHr
                if(tweetHr<firstHour):
                    firstHour=tweetHr

                #######If this is the first sample in the file#######
                if firstTweet:
                    firstTweet = False
                    curTweetHr = tweetHr
                    curDayHr = dayHr

                    #Update count depending on whether this is a tweet or re-tweet
                    [tweetCount, retweetCount] = resetCount(tweet)

                    followerSum = int(tweet['original_author']['followers'])
                    followerMax = int(tweet['original_author']['followers'])

                    impCount = int(tweet['metrics']['impressions'])

                #######If we find more (re-)tweets in this hour#######
                elif tweetHr == curTweetHr:

                    #Update count depending on whether this is a tweet or re-tweet
                    [tweetCount, retweetCount] = updateCount(tweet, tweetCount, retweetCount)

                    followerSum = followerSum + int(tweet['original_author']['followers'])
                    followerMax = max(followerMax, int(tweet['original_author']['followers']))

                    impCount = max(impCount, int(tweet['metrics']['impressions']))

                #######If it's time to move onto the next hour#######
                else:
                    testList.append(
                        [curTweetHr, tweetCount, retweetCount, followerSum, followerMax, curDayHr, impCount])

                    curTweetHr = tweetHr
                    curDayHr = dayHr

                    [tweetCount, retweetCount] = resetCount(tweet)

                    followerSum = int(tweet['original_author']['followers'])
                    followerMax = int(tweet['original_author']['followers'])

                    impCount = int(tweet['metrics']['impressions'])

    testList.append(
        [curTweetHr, tweetCount, retweetCount, followerSum, followerMax, curDayHr, impCount])
    testList.remove([])
    return [testList,firstHour,lastHour]


#Number of hashtags to sweep
nTag = len(config.input_file_list)

#cross validation on the training data and choose the best model
statList = [[[]] for x in range(nTag)]
for cnt in range(nTag):
    new_data = np.load(str(cnt)+'.txt.npy')
    statList[cnt] = new_data
    # print len(statList[cnt])
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
timeBasedModels = {1:[394796,395215],2: [395216, 395228], 3: [395228,395367]}

# based on the model needed we can choose the initial start hour and end hour.
startHr = timeBasedModels[3][0]
endHr = timeBasedModels[3][1]
i=startHr
#Need an intercept, so we add a column of 1's
#X - array of data, row corresponds to data sample, and column corresponds to feature dimension (X = sm.add_constant(X))
#y - functional output vector with same number of rows as X
#numHours - number of hours to run the model on
numHours = endHr-startHr
print numHours
X = [[1,0,0,0,0] for a in range(nTag*numHours)]
y = [0 for b in range(nTag*numHours)]

#Extract the relevant data for next-hour prediction
for j in range(nTag):
    for k in range(numHours):
        rec1 = [r for r in statList[j] if r[0] == (i+k)]
        if rec1 != []:
            X[j*numHours + k][1] = rec1[0][2]    #sum of retweets
            X[j*numHours + k][2:5] = rec1[0][4:7]
            y[j*numHours + k] = rec1[0][1]
print X
print y
X= np.array(X)
y = np.array(y)
# cross validation indices given by scikit shuffle split
ss = cross_validation.ShuffleSplit(n=6*numHours, n_iter=10, test_size=0.1, random_state=699)
print ss
cnt = 0
olsErrorMetric=[]
glsErrorMetric=[]
olsErrorMetricPerSample=[]
glsErrorMetricPerSample=[]

for train_index, test_index in ss:
    model = sm.OLS(y[train_index], X[train_index])
    results = model.fit()
    res_cv = results.predict(X[test_index])
    # print(res_cv)
    # print(y[test_index])
    nError = np.subtract(res_cv, y[test_index])
    # print nError
    finalError = np.sum(np.absolute(nError))
    print "Iteration" + str(cnt)
    cnt=cnt+1
    print(finalError)
    print(finalError/len(test_index))
    olsErrorMetric.append(finalError)
    olsErrorMetricPerSample.append(finalError/len(test_index))
    #GLS - generalized LS: errors are independent but heteroscedastic (different variance)
    #Fit & save statistical information
    residVar = np.diag([a ** 2 for a in results.resid])
    #round the values of the residual covariance matrix to avoid inversion of singular matrices
    residVar = [[round(a2, 4) for a2 in a1] for a1 in residVar]
    #can perform GLS if the residual covariance matrix is invertible
    if isPD(residVar):
        model = sm.GLS(y[train_index], X[train_index], residVar)
        results = model.fit()
        res_cv = results.predict(X[test_index])
        nError = np.subtract(res_cv, y[test_index])
        finalError_GLS = np.sum(np.absolute(nError))
        print(finalError_GLS)
        print(finalError_GLS/len(test_index))
        if(len(glsErrorMetric) > 0 and finalError_GLS > np.amax(glsErrorMetric)):
            final_model = results
        elif(len(glsErrorMetric) == 0):
            final_model = results
        glsErrorMetric.append(finalError_GLS)
        glsErrorMetricPerSample.append(finalError_GLS/len(test_index))

# calculating the predictions with the selected model from the given test data
for file_name in ['/opt/ee239/sample3_period3.txt',
                   '/opt/ee239/sample7_period3.txt',
                   '/opt/ee239/sample10_period3.txt']:
    [testList,firstHour, lastHour] = getTestData(file_name)
    # print(len(testList[0][1]))
    i=firstHour
    numHours = lastHour-firstHour
    print(numHours)
    X_test = [[1,0,0,0,0] for a in range(numHours)]
    j=0;
    #Extract the relevant data for next-hour prediction
    for k in range(numHours):
        rec1 = [r for r in testList if r[0] == (i+k)]
        if rec1 != []:
            X_test[k][1] = rec1[0][2]    #sum of retweets
            X_test[k][2:5] = rec1[0][4:7]
    next_hr_result = final_model.predict(X_test)
    result = np.average(next_hr_result)
    print file_name
    print result