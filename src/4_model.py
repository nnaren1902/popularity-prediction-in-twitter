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

#Number of hashtags to sweep
nTag = len(config.input_file_list)

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
#PST to UTC

#writing output to a file
outputFH1 = open('../log/part4_results2.txt','w')
outputFH2 = open('../log/part5_results.txt','w')

#based on models needed choose the hours
startHr = timeBasedModels[1][0]
endHr = timeBasedModels[1][1]
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
X= np.array(X)
y = np.array(y)
# cross validation indices given by scikit shuffle split
ss = cross_validation.ShuffleSplit(n=6*numHours, n_iter=10, test_size=0.1, random_state=699)
cnt = 0
olsErrorMetric=[]
glsErrorMetric=[]
olsErrorMetricPerSample=[]
glsErrorMetricPerSample=[]


# training and cross validating the models
for train_index, test_index in ss:
    model = sm.OLS(y[train_index], X[train_index])
    results = model.fit()
    res_cv = results.predict(X[test_index])
    nError = np.subtract(res_cv, y[test_index])
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

# writing the outputs to files.
for cnt in range(10):
    outputFH1.write(str(olsErrorMetric[cnt])+", "+str(olsErrorMetricPerSample[cnt])+", "+str(glsErrorMetric[cnt])+ ", "+str(glsErrorMetricPerSample[cnt])+ "\n")
outputFH1.write("Average Error: "+"\n")
outputFH1.write(str(np.sum(olsErrorMetric)/10) +", "+str(np.sum(olsErrorMetricPerSample)/10)+", "+str(np.sum(glsErrorMetric)/10) +", "+str(np.sum(glsErrorMetricPerSample)/10)+"\n")


outputFH1.write("")
outputFH1.close()
outputFH2.close()