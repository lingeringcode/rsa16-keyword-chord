import csv,json,argparse

# parser
# parser = argparse.ArgumentParser(usage="-h for full usage")
# parser.add_argument('-i', dest="input", help='Path to JSON file to read',required=False)
# parser.add_argument('-o', dest="output", help='CSV file name to save results',required=False)
# args = parser.parse_args()
# f = args.input
# output = args.output

# Open the CSV
f = open( 'rsa16-tweets-full-0531.csv', 'rU' )
# Change each fieldname to the appropriate field name.
reader = csv.DictReader( f, fieldnames = ( "id_str","from_user","text","created_at",
	"time","geo_coordinates","user_lang","in_reply_to_user_id_str","in_reply_to_screen_name",
	"from_user_id_str","in_reply_to_status_id_str","source","profile_image_url",
	"user_followers_count","user_friends_count","status_url","entities_str" ))
# Parse the CSV into JSON
out = json.dumps( [ row for row in reader ] )
print out
print "JSON parsed!"
# Save the JSON
# f = open( 'rsa16-tweets-full-0531.json', 'w')
# f.write(out)
# print "JSON saved!"