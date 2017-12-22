
#####################################################################
### Assignment skeleton
### You can alter the below code to make your own dynamic website.
### The landing page for assignment 3 should be at /
#####################################################################

from bottle import route, run, default_app, debug
from copy import deepcopy
import a2
meta1=[]
content1=[]
letters="ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZabcçdefgğhıijklmnoöprsştuüvyz9876543210-' "
trans={i:letters.index(i) for i in letters}
#~ def htmlify(title,text):
    #~ page = """
        #~ <!doctype html>
        #~ <html lang="en">
            #~ <head>
                #~ <meta charset="utf-8" />
                #~ <title>%s</title>
            #~ </head>
            #~ <body>
            #~ %s
            #~ </body>
        #~ </html>

    #~ """ % (title,text)
    #~ return page
def split_contents():
	global meta1,content1
	meta1=a2.contents[:a2.find_starting_point("total",a2.contents)+1]
	content1=a2.contents[a2.find_starting_point("total",a2.contents)+1:]

def look_at_this_dude(li):
	return ([trans.get(li[0][i]) for i in range(len(li[0]))])

def index():
	return a2.template %(a2.title(),a2.make_table(a2.contents))

def sort_by_what(a,b):
	split_contents()
	global meta1, content1
	meta,content=deepcopy(meta1),deepcopy(content1)
	data=[]
	if a=="name":
		if b=="True":
			meta[a2.find_starting_point("total",meta1)-1][0]="( &Delta; ) " +meta[a2.find_starting_point("total",meta1)-1][0]
			b="Ascending"
			data+=sorted(content,key=look_at_this_dude)
		else:
			meta[a2.find_starting_point("total",a2.contents)-1][0]="( &nabla; ) " +meta[a2.find_starting_point("total",a2.contents)-1][0]
			b="Descending"
			data+=reversed(sorted(content,key=look_at_this_dude))
		a="Province Name"

	else:
		content.sort(key = lambda x : x[a2.find_starting_point(a,a2.contents)])
		if b=="True":
			meta[a2.find_starting_point("total",a2.contents)-1][a2.find_starting_point(a,a2.contents)]="( &Delta; ) " + meta[a2.find_starting_point("total",a2.contents)-1][a2.find_starting_point(a,a2.contents)]
			b="Ascending"
			data+=content
		else:
			meta[a2.find_starting_point("total",a2.contents)-1][a2.find_starting_point(a,a2.contents)]="( &nabla; ) " + meta[a2.find_starting_point("total",a2.contents)-1][a2.find_starting_point(a,a2.contents)]
			b="Descending"
			data+=reversed(content)
		if a=="pop":
			a="Population"
		elif a == "in":
			a="In-migration"
		elif a == "out":
			a="Out-migration"
		elif a == "net":
			a="Net migration"
		else:
			a="Rate of Net Migration"
	data=meta+data
	return a2.template %("Sorted by %s in %s Order "%(a,b),a2.make_table(data))
		



route('/', 'GET', index)
route('/sort/<a>/<b>', 'GET' ,sort_by_what)

#####################################################################
### Don't alter the below code.
### It allows this website to be hosted on Heroku
### OR run on your computer.
#####################################################################

# This line makes bottle give nicer error messages
debug(True)
# This line is necessary for running on Heroku
app = default_app()
# The below code is necessary for running this bottle app standalone on your computer.
if __name__ == "__main__":
	run()

