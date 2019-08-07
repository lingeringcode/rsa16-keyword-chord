import re,sys,csv,json,collections,nltk

'''#######################################
# Parses merged keyword corpora with particular keywords in mind
# Specifically, it parses the related words column 
# and consolidates plurals and related words.
# For example:
#   If embodiment or bodies is found, change to embodied.
#   If disabilities is found, change to disability.
#   If machines is found, change to machine.
# Outputs cleaned file as another CSV.
#######################################'''

csv_file_in = "output/sk-merged-6.csv" #name your csv file/input here
csv_file_out = "output/sk-merged-6-1.csv" #name your csv file/input here
dis = 'disability'
bod = 'embodied'
fem = 'feminist'
black = 'black'
white = 'white'
machine = 'machine'

# source words for consolidation
re_source_feminist      = re.compile(r'(fem\S*)', re.IGNORECASE)
re_source_latinx        = re.compile(r'((latin\S*))', re.IGNORECASE)
re_source_material      = re.compile(r'(material\S*)', re.IGNORECASE)
re_source_embodied      = re.compile(r'((\bbod\S*)|(embodi\S*))', re.IGNORECASE)
re_source_disability    = re.compile(r'((disab\S*)|(\bable\S*))', re.IGNORECASE)
re_source_black         = re.compile(r'(black\S*)', re.IGNORECASE)
re_source_white         = re.compile(r'(white\S*)', re.IGNORECASE)
re_source_machine       = re.compile(r'(machine|machines)', re.IGNORECASE)
    

# loads CSV, checks for source_word, then calls 
def load_and_check():
    reader = csv.reader(open(csv_file_in, 'rb'))
    writer = csv.writer(open(csv_file_out, 'wb'), lineterminator='\r\n', quoting=csv.QUOTE_ALL)
    for row in reader:
        # check every row ignoring the particular source word
        if re_source_disability.match(row[1]):
            row[1] = dis
            writer.writerow([row[0], row[1], row[2]])
        if re_source_feminist.match(row[1]):
            row[1] = fem
            writer.writerow([row[0], row[1], row[2]])
        if re_source_embodied.match(row[1]):
            row[1] = bod
            writer.writerow([row[0], row[1], row[2]])
        if re_source_white.match(row[1]):
            row[1] = white
            writer.writerow([row[0], row[1], row[2]])
        if re_source_machine.match(row[1]):
            row[1] = machine
            writer.writerow([row[0], row[1], row[2]])
        else:
            writer.writerow([row[0], row[1], row[2]])

def main():
    load_and_check()

if __name__ == '__main__':
    main()