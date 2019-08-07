import re,sys,csv,json,collections

'''#######################################
# Parses all words in tweets in source corpus
# and generates a data set w/ follwoing:
#   1. word
#   2. Number of times word used
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
ITEM_MAX = 2000 #enter optional limit to indexing common words
json_file_in = "../source/rsa16-tweets-full-0531.json" #name your json file/input here
csv_file_out = "../../rsa16bubble/assets/data/rsa16-word-counts-full.csv" #name your new/output file here

def tally_words():
    for tweets in json.load(open(json_file_in)):
        for word in re_word.findall(tweets['text'].lower()):
            if len(word) > 2 and word not in stopwords:
                words[word] += 1

def write_word_count():
    with open(csv_file_out, 'wb') as c:
        writer = csv.writer(c, lineterminator='\r\n')
        writer.writerow(['word', 'count'])
        for word, count in reversed(words.most_common(ITEM_MAX)):
            writer.writerow([word.encode('utf8'), count])

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
    tally_words()
    write_word_count()
    append_id_column(csv_file_out)

if __name__ == '__main__':
    main()