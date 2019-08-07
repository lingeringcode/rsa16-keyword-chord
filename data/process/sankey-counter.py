import re,sys,csv,json,collections

'''#######################################
# Parses source corpus of tweets for keyword
# and generates a new data set w/ follwoing:
#   1. Keyword as source word.
#   2. Found related words in tweets, if not in stopwords.
#   3. A count of that particular related word.
#######################################'''

stopwords = set([ "rt","teh","i","me","my","myself","we","us","#rsa16","rsa16","http","amp","like",
                                "our","ours","ourselves","you","your","yours","yourself","just","dont",
                                "yourselves","he","him","his","himself","she","her","hers","wouldn",
                                "herself","it","its","itself","they","them","their","theirs","ways",
                                "themselves","what","which","who","whom","whose","this","get",
                                "that","these","those","am","is","are","also","was","were","be","been",
                                "being","have","has","had","having","do","does","did","doing",
                                "will","would","should","can","could","ought","i'm","you're","he's",
                                "she's","it's","we're","they're","i've","you've","we've","they've",
                                "i'd","you'd","he'd","she'd","we'd","they'd","i'll","you'll","he'll",
                                "she'll","we'll","they'll","isn't","aren't","wasn't","weren't","hasn't",
                                "haven't","hadn't","doesn't","don't","didn't","won't","wouldn't","wont",
                                "shouldn't","can't","cannot","couldn't","mustn't","let's","that's","who's",
                                "what's","here's","there's","when's","where's","why's","how's","a","an",
                                "the","and","but","if","or","because","as","until","while","of","at","by","for",
                                "with","about","against","between","into","through","during","before","after",
                                "above","below","to","from","up","upon","down","in","out","on","off","over",
                                "under","again","further","then","once","here","there","when","where",
                                "why","how","all","any","both","each","few","more","most","other","some",
                                "such","no","nor","not","only","own","same","so","than","too","very","say",
                                "says","said","shall","https","one","presentation","now","way","hey","fri",
                                "well","yet","friday","2013","since"])

re_word = re.compile(r'[a-z0-9\']+')
words = collections.Counter()
# enter word to analyze
# if using re_mult_source_word, use as the source variable name
source_word = 'c17'
re_mult_source_word = re.compile(r'(c17)', re.IGNORECASE)

'''#######################################
# Stockpile of regex patterns
# re.compile(r'(material\S*)', re.IGNORECASE)
# re.compile(r'(fem\S*)', re.IGNORECASE)
# re.compile(r'((\brac\S*)))', re.IGNORECASE)
# re.compile(r'((\bbod\S*)|(embodi\S*))', re.IGNORECASE)
# re.compile(r'(disab\S*)|(\bable\S*))', re.IGNORECASE)
# re.compile(r'(access|accessibility|inaccessible|accessibility|accessible)', re.IGNORECASE)
# re.compile(r'(institution|institutional|institutionalized|institutionalization|institutionally)', re.IGNORECASE)
# re.compile(r'(public\S*)', re.IGNORECASE)
# re.compile(r'(\bsex\S*|\bbisex\S*|\bheterosex\S*|\bcishet)', re.IGNORECASE)
# re.compile(r'(method\S*)', re.IGNORECASE)
# re.compile(r'((\bobj\S*|ooo))', re.IGNORECASE)
# re.compile(r'((\bdig\S*))', re.IGNORECASE)
# re.compile(r'((\bmemor\S*))', re.IGNORECASE)
# re.compile(r'(\bmachin\S*)', re.IGNORECASE)
# re.compile(r'(\bwomen|woman)', re.IGNORECASE)
# re.compile(r'(masculin\S*)', re.IGNORECASE)
# re.compile(r'(\bintersection\S*)', re.IGNORECASE)
#######################################'''

tweet_total = 0
ITEM_MAX = 3000 #enter optional limit to indexing common words
json_file_in = "../source/rsa16-tweets-full-0531.json" #name your json file/input here
csv_file_out = "output/cfshrc/sk-c17.csv" #name your new/output file here
csv_twt_file_out = "output/cfshrc/sk-c17-tweets.csv" #name your new/output file here

# pluralizes words
def plural(word):
    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word[-1] in 'sx' or word[-2:] in ['sh', 'ch']:
        return word + 'es'
    elif word.endswith('an'):
        return word[:-2] + 'en'
    return word + 's'

# tallies words in tweet
def tally_associated_words(tweet_to_tally):
    for word in re_word.findall(tweet_to_tally):
            if len(word) > 2 and word not in stopwords:
                words[word] += 1
                write_sankey_count

# loads JSON, checks for source_word, then calls tally
def load_and_check():
    for tweets in json.load(open(json_file_in)):
        tweet_to_tally = tweets['text'].lower()

        if 're_mult_source_word' in globals():
            ttt = re_mult_source_word.search(tweet_to_tally)
            if ttt is not None:
                print (tweets['id_str'], tweets['text'] ) # check if re is working
                with open(csv_twt_file_out, 'a') as t:
                    twt_writer = csv.writer(t, lineterminator='\r\n', quoting=csv.QUOTE_ALL)
                    # writer.writerow(['tw_id', 'tweet'])
                    twt_writer.writerow([ tweets['id_str'].encode(), tweet_to_tally.encode('utf8') ])

                tally_associated_words(tweet_to_tally)

        # if 'source_words' in globals():
        #     for keyword in source_words:
        #         # print tweet_to_tally
        #         with open(csv_twt_file_out, 'a') as t:
        #             twt_writer = csv.writer(t, lineterminator='\r\n', quoting=csv.QUOTE_ALL)
        #             # writer.writerow(['tw_id', 'tweet'])
        #             twt_writer.writerow([ tweets['id_str'].encode(), tweet_to_tally.encode('utf8') ])

        #         tally_associated_words(tweet_to_tally)

        # else:
        #     if source_word in tweet_to_tally:
        #         # print tweet_to_tally
        #         with open(csv_twt_file_out, 'a') as t:
        #             twt_writer = csv.writer(t, lineterminator='\r\n', quoting=csv.QUOTE_ALL)
        #             # writer.writerow(['tw_id', 'tweet'])
        #             twt_writer.writerow([ tweets['id_str'].encode(), tweet_to_tally.encode('utf8') ])

        #         tally_associated_words(tweet_to_tally)

# Adds sankey entry to collection
def write_sankey_count():
    with open(csv_file_out, 'wb') as c:
        writer = csv.writer(c, lineterminator='\r\n', quoting=csv.QUOTE_ALL)
        writer.writerow(['source', 'related', 'count'])
        for word, count in reversed(words.most_common(ITEM_MAX)):
            if count > 0:
                writer.writerow([source_word.encode('utf8'), word.encode('utf8'), count])

# if an ID is necessary, this appends one to each entry
def append_id_column(csv_file_out):
    
    f = open(csv_file_out, 'r')
    contents = f.readlines()
    f.close()

    reader = csv.reader(contents)

    f = open(csv_file_out, 'wb')
    writer = csv.writer(f)

    header = reader.next()
    header.append('id')
    writer.writerow(header)

    the_id = 0
    for row in reader:
        the_id += 1
        row.append(the_id)
        writer.writerow(row)

    f.close()

def main():
    load_and_check()
    write_sankey_count()
    # append_id_column(csv_file_out)

if __name__ == '__main__':
    main()