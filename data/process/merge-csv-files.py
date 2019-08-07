'''
# Merges csv files in list into one CSV to rule them all.
'''

# create list of filenames
filenames = ["invisible","race","latinx","white"]

# create output file
fout=open("output/sk-merged-race.csv","a")

# write first file:
for line in open("output/sk-black.csv"):
    fout.write(line)

# now the rest:    
for name in filenames:
    f = open("output/sk-" + name + ".csv")
    print f
    f.next() # skip the header
    for line in f:
         fout.write(line)
    f.close() # not really needed

fout.close()
