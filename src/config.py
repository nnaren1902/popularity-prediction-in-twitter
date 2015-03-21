import datetime

input_file_list = ['/opt/ee239/tweets_#gohawks.txt',
                   '/opt/ee239/tweets_#nfl.txt',
                   '/opt/ee239/tweets_#sb49.txt',
                   '/opt/ee239/tweets_#gopatriots.txt',
                   '/opt/ee239/tweets_#patriots.txt',
                   '/opt/ee239/tweets_#superbowl.txt']

test_file_list = ['/opt/ee239/sample1_period1.txt',
                   '/opt/ee239/sample4_period1.txt',
                   '/opt/ee239/sample5_period1.txt',
                   '/opt/ee239/sample8_period1.txt']
test_file_list_2 = ['/opt/ee239/sample6_period2.txt']
test_file_list_3 = [
                   '/opt/ee239/sample3_period3.txt',
                   '/opt/ee239/sample7_period3.txt',
                   '/opt/ee239/sample10_period3.txt'
                   ]

output_file_list1 = {'/opt/ee239/tweets_#gohawks.txt':'../output/part1/#gohawks_stats.txt' ,'/opt/ee239/tweets_#nfl.txt':'../output/part1/#nfl_stats.txt' , '/opt/ee239/tweets_#sb49.txt':'../output/part1/#sb49_stats.txt' , '/opt/ee239/tweets_#gopatriots.txt':'../output/part1/#gopatriots_stats.txt', '/opt/ee239/tweets_#patriots.txt':'../output/part1/#patriots_stats.txt' , '/opt/ee239/tweets_#superbowl.txt':'../output/part1/#superbowl_stats.txt'};
output_file_list2 = {'/opt/ee239/tweets_#gohawks.txt':'../output/part1/#gohawks_avgs.txt' ,'/opt/ee239/tweets_#nfl.txt':'../output/part1/#nfl_avgs.txt' , '/opt/ee239/tweets_#sb49.txt':'../output/part1/#sb49_avgs.txt' , '/opt/ee239/tweets_#gopatriots.txt':'../output/part1/#gopatriots_avgs.txt', '/opt/ee239/tweets_#patriots.txt':'../output/part1/#patriots_avgs.txt' , '/opt/ee239/tweets_#superbowl.txt':'../output/part1/#superbowl_avgs.txt'};
delta = datetime.timedelta(hours=1);

input_file_order = {'/opt/ee239/tweets_#gohawks.txt':0,'/opt/ee239/tweets_#nfl.txt':1,'/opt/ee239/tweets_#sb49.txt':2,'/opt/ee239/tweets_#gopatriots.txt':3,'/opt/ee239/tweets_#patriots.txt':4,'/opt/ee239/tweets_#superbowl.txt':5}

test_file_order = {'/opt/ee239/sample1_period1.txt':0,
                   '/opt/ee239/sample4_period1.txt':1,
                   '/opt/ee239/sample5_period1.txt':2,
                   '/opt/ee239/sample8_period1.txt':3}
test_file_order_2 = {'/opt/ee239/sample2_period2.txt':2,
                   '/opt/ee239/sample9_period2.txt':1,
                   '/opt/ee239/sample6_period2.txt':0}