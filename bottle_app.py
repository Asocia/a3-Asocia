
#####################################################################
### Assignment skeleton
### You can alter the below code to make your own dynamic website.
### The landing page for assignment 3 should be at /
#####################################################################

from bottle import route, run, default_app, debug, static_file, request
from copy import deepcopy
import a2
meta1=[]
content1=[]
letters="ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZabcçdefgğhıijklmnoöprsştuüvyz9876543210-' "
trans={i:letters.index(i) for i in letters}
navbar="""<ul>
  <li><a class="active" href="/">Home</a></li>
  <li><a href="/sort">Sort by...</a></li>
  <li><a href="#filter">Filter</a></li>
  <li><a href="#login">Login</a></li>
</ul>
<br>"""
def split_contents():
	global meta1,content1
	meta1=a2.contents[:a2.find_starting_point("total",a2.contents)+1]
	content1=a2.contents[a2.find_starting_point("total",a2.contents)+1:]

def look_at_this_dude(li):
	return ([trans.get(li[0][i]) for i in range(len(li[0]))])

def index():
	
	return a2.template %{'title':a2.title(),'navbar':navbar,'table':a2.make_table(a2.contents),'form':""}
#~ def sort_by_page():
	
	
	#~ return a2.template %{'title':a2.title(),'navbar':navbar,'table':a2.make_table(a2.contents),'form':form}
def sort_by_what():
	try:
		a=request.GET['a']
	except KeyError:
		a="name"
	try:
		b=request.GET['b']
	except KeyError:
		b="True"
	di={'name':"",'pop':"",'in':"",'ao':"checked",'do':"",'out':"",'net':"",'rate':""}
	for i in di.keys():
		if a==i:
			di[i]="selected"
			break
	if b!="True":
		di["ao"],di["do"]=di["do"],di["ao"]
	
	form="""<form action="/sort" method="GET">Sort by
                <select name="a">
                    <option value="name" %(name)s>Province name</option>
                    <option value="pop" %(pop)s>Total population</option>
                    <option value="in" %(in)s>In-migration</option>
                    <option value="out" %(out)s>Out-migration</option>
                    <option value="net" %(net)s>Net migration</option>
                    <option value="rate" %(rate)s>Rate of net migration</option> 
                </select> in
                <input type="radio" name="b" value="True" %(ao)s>ascending order.
                <input type="radio" name="b" value="False" %(do)s>descending order.
                <input type="submit" value="Apply" />
             </form>"""%di
             
	split_contents()
	global meta1, content1
	meta,content=deepcopy(meta1),deepcopy(content1)
	data=[]
	if 'a' in request.GET:
		a=request.GET['a']
		b="True"
	else:
		return a2.template %{'title':a2.title(),'navbar':navbar,'table':a2.make_table(a2.contents),'form':form}
	if 'b' in request.GET:
		b=request.GET['b']
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
	return a2.template %{'title':"Sorted by %s in %s Order "%(a,b),'navbar':navbar,'form':form,'table':a2.make_table(data)}
		
def server_static(path):
	return static_file(path, root=".")



route('/', 'GET', index)
route('/sort', 'GET' , sort_by_what)
route('/static/<path>', 'GET', server_static)

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

