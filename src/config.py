import datetime

input_file_list = ['../../train_data/tweets_#gohawks.txt','../../train_data/tweets_#nfl.txt','../../train_data/tweets_#sb49.txt','../../train_data/tweets_#gopatriots.txt' , '../../train_data/tweets_#patriots.txt', '../../tweet_data/train_#superbowl.txt' ]

output_file_list1 = {'../../tweet_data/tweets_#gohawks.txt':'../output/part1/#gohawks_stats.txt' ,'../../tweet_data/tweets_#nfl.txt':'../output/part1/#nfl_stats.txt' , '../../tweet_data/tweets_#sb49.txt':'../output/part1/#sb49_stats.txt' , '../../tweet_data/tweets_#gopatriots.txt':'../output/part1/#gopatriots_stats.txt', '../../tweet_data/tweets_#patriots.txt':'../output/part1/#patriots_stats.txt' , '../../tweet_data/tweets_#superbowl.txt':'../output/part1/#superbowl_stats.txt'};
output_file_list2 = {'../../tweet_data/tweets_#gohawks.txt':'../output/part1/#gohawks_avgs.txt' ,'../../tweet_data/tweets_#nfl.txt':'../output/part1/#nfl_avgs.txt' , '../../tweet_data/tweets_#sb49.txt':'../output/part1/#sb49_avgs.txt' , '../../tweet_data/tweets_#gopatriots.txt':'../output/part1/#gopatriots_avgs.txt', '../../tweet_data/tweets_#patriots.txt':'../output/part1/#patriots_avgs.txt' , '../../tweet_data/tweets_#superbowl.txt':'../output/part1/#superbowl_avgs.txt'};
delta = datetime.timedelta(hours=1);

input_file_order = {'../../train_data/tweets_#gohawks.txt':0,'../../train_data/tweets_#nfl.txt':1,'../../train_data/tweets_#sb49.txt':2,'../../train_data/tweets_#gopatriots.txt':3,'../../train_data/tweets_#patriots.txt':4,'../../train_data/tweets_#superbowl.txt':5}