import common as common
import config as config
import numpy as np
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
for cnt in range(nTag):
    new_data = np.load(str(cnt)+'.txt.npy')
    statList[cnt] = new_data
    print len(statList[cnt])

print len(statList)