import sys,json,csv,codecs,argparse,re,datetime
import pandas as pd
from datetime import datetime
from time import strptime

'''#######################################
# Parses main corpus of tweets with keyword as a filter
# If keyword found in tweet, it adds the following to a CSV:
# 	Tweet ID, Tweet content, Time of tweet
#######################################'''

# globals
json_file = "../source/rsa16-tweets-full-0531.json" # change to your input/json file
time = []
kwtweet = []
tweet_id = []
archive_content = []
# re_mult_source_word = 

'''#######################################
# Stockpile of regex patterns
# re.compile(r'(feminis?m|feminis?t)', re.IGNORECASE)
# re.compile(r'(embodi?ed|embodi?ment)', re.IGNORECASE)
# re.compile(r'(machin\S*|ooo|object)', re.IGNORECASE)
# re.compile(r'(machin\S*|ooo|object\S*)', re.IGNORECASE)
# re.compile(r'(racis?m|race|racis?t|white|white?ness|latina|latino|latinx|asian|black|black?ness)', re.IGNORECASE)
#######################################'''


#parser
parser = argparse.ArgumentParser(usage="-h for full usage")
parser.add_argument('-k', dest="keyword", help='keyword to search twitter corpus, e.g. rhetoric',required=True)
# parser.add_argument('-output', dest="output", help='CSV file name to save results',required=False)
args = parser.parse_args()
keyword = args.keyword
# filename = args.output


f = open(keyword+"_rsaCount.csv", 'wb')
writer = csv.writer(f, lineterminator='\r\n')
writer.writerow(['id','time','kwtweet'])

def prime_writer():

	with codecs.open(json_file, encoding="utf-8-sig") as data_file:
		data = json.load(data_file)
	return data

def get_tweets(archive_content, keyword):

	for tweet in archive_content:
		
		'''##############################
			if time needs formatting help
		'''##############################
		# dirty_time = tweet['created_at'].encode('utf-8')
		# new_time = date_formatter(dirty_time)
		# time = new_time

		time = tweet['created_at'].encode('utf-8')
		tweet_id_check = tweet['id_str'].encode('utf-8')
		kwtweet = tweet['text'].lower().encode('utf-8')
		# Replace linebreaks w/ space
		rm_newline_kwtweet = kwtweet.replace('\n', ' ').replace('\r', '')

		if 're_mult_source_word' in globals():
			if tweet_id_check not in tweet_id:
				ttt = re_mult_source_word.search(rm_newline_kwtweet)
				tweet_id.append(tweet['id_str'].encode('utf-8')) # build id checklist
				if ttt is not None:
					written_csv = writer.writerow([tweet_id_check, time, rm_newline_kwtweet])
		elif 're_mult_source_word' not in globals():
			if tweet_id_check not in tweet_id:
				tweet_id.append(tweet['id_str'].encode('utf-8')) # build id checklist
				if keyword in rm_newline_kwtweet:
					written_csv = writer.writerow([tweet_id_check, time, rm_newline_kwtweet])
	
	return written_csv

def date_formatter(dirty_time):
	# Tue May 31 12:08:49 +0000 2016
	clean_time = re.sub(('\+0000 '), (r''), dirty_time)
	a = re.compile("^([0-9])")

	if a.match(clean_time):
		clean_time = re.sub(('T'), (r' '), dirty_time)
		clean_time = datetime.strptime(clean_time, '%Y-%m-%d %H:%M:%S')

	else:
		clean_time = datetime.strptime(clean_time, '%c')

	return clean_time

def main():
	archive_content = prime_writer()
	get_tweets(archive_content, keyword)

if __name__ == '__main__':
	main()