
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
  <li><a href="/search">Search a Province</a></li>
  <li><a href="/sort">Sort by...</a></li>
  <li><a href="/filter">Filter</a></li>
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
	form="""<form action="/sort" method="GET" >Sort by
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
             </form><br>"""%di
	split_contents()
	global meta1, content1
	meta,content=deepcopy(meta1),deepcopy(content1)
	data=[]
	if 'a' in request.GET:
		a=request.GET['a']
		b="True"
	else:
		return a2.template %{'title':'Sort by...','navbar':navbar,'table':a2.make_table(a2.contents),'form':form}
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
def search_province():
	form="""<form action="/search" method="GET" class="simple-form" >
	
                <input size="45" type="search" placeholder="Please enter at least 2 characters. (Only in English) " pattern="[A-Za-z]{2,}" required name="province">
                <input type="submit" value="Search" />
             </form><br>"""
	try:
		name=request.GET['province'].lower()
	except KeyError:
		name=""
	if name =="":
		return a2.template %{'title':"Search a Province",'navbar':navbar,'table':a2.make_table(a2.contents),'form':form}
	split_contents()
	global content1,meta1
	meta,content=deepcopy(meta1)[:a2.find_starting_point("total",a2.contents)+1],deepcopy(content1)
	data=[]
	for row in content:
		if name.lower() in row[0].replace('İ','i').lower().replace('ç','c').replace('ğ','g').replace('ı','i').replace('ö','o').replace('ş','s').replace('ü','u'):
			if name.lower()== row[0][:len(name.lower())].replace('İ','i').lower().replace('ç','c').replace('ğ','g').replace('ı','i').replace('ö','o').replace('ş','s').replace('ü','u'):
				data=[row]+data
			else:
				data+=[row]
	data=meta+data
	if data==meta:
		return a2.template %{'title':"Searching Result",'navbar':navbar,'form':form,'table':"<p>No records were found that match the specified search crieteria :( <a href=\"/search\"> See full table...</a></p>"}
	a2.calculate_the_cells(data)
	return a2.template %{'title':"Searching Result",'navbar':navbar,'form':form,'table':a2.make_table(data)}

def get_filter_criterias():
	form="""<form action="/set+filter+conditions" method="POST" >Please select filtering criteria(s):<br>
                
                    <input type="checkbox" name="name" value="name">Province name<br>
                    <input type="checkbox" name="pop" value="pop">Total population<br>
                    <input type="checkbox" name="in" value="in">In-migration<br>
                    <input type="checkbox" name="out" value="out">Out-migration<br>
                    <input type="checkbox" name="net" value="net">Net migration<br>
                    <input type="checkbox" name="rate" value="rate">Rate of net migration<br>
                    <input type="submit" value="Apply" />
             </form><br>"""
	return a2.template %{'title':"Filter Criteria...",'navbar':navbar,'form':form,'table':a2.make_table(a2.contents)}

def get_filter_cond():
	return 'Şimdi uykum var, yarın gel söylicem.'
	#~ """
	#~ <form action="/filterasd" method="POST">Please specify filter condition(s):<br>
	#~ %(name)s <br>
	#~ %(pop)s <br>
	#~ %(in)s <br>
	#~ %(out)s <br>
	#~ %(net)s <br>
	#~ %(rate)s <br>
	#~ """
	#~ di={'name':"",'pop':"",'in':"",'out':"",'net':"",'rate':""}
	#~ for i in di.keys():
		#~ if type(request.POST.get(i)) is str:
			#~ di[i]="+"
	
			
	#~ if type(request.POST.get("name")) is str:
		#~ f_listrequest.POST.get("name")
	
	#~ name=request.POST.get("name")
	#~ pop=request.POST.get("pop")
	#~ inm=request.POST.get("in")
	#~ out=request.POST.get("out")
	#~ net=request.POST.get("net")
	
		#~ print(type(request.POST.get("name")))
	
	
	#~ return name+pop+inm+out+net
def server_static(path):
	return static_file(path, root=".")







#~ def test():
	#~ html="""<form action='/biseyler' method='POST'>
	#~ <input name="name" type='text'>
	#~ <input type='submit' value='submit'>
	#~ </form>
	#~ """
	#~ return html
#~ def myfunc():
	
	#~ print(len(request.POST))
	#~ return 'oha oldu laaaaannnn!'
#~ route('/test','GET', test)
#~ route('/biseyler','POST', myfunc)













route('/search', 'GET', search_province)
route('/', 'GET', index)
route('/sort', 'GET', sort_by_what)
route('/filter', 'GET', get_filter_criterias)
route('/set+filter+conditions', 'POST', get_filter_cond)
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

