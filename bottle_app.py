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
tr="ÇĞİÖŞÜçğıöşü"
en="CGIOSUcgiosu"
col_names={"name":"Province name","pop":"Population","in":"In-migration","out":"Out-migration","rate":"Rate of net migration","net":"Net migration"}
tr_to_en={tr[i]:en[i] for i in range(len(tr))}
trans={i:letters.index(i) for i in letters}
navbar="""<ul>
		<li><a class="active" href="/">Home</a></li>
		<li><a href="/search">Search a Province</a></li>
		<li><a href="/sort">Sort by...</a></li>
		<li><a href="/filter">Filter</a></li>
		<li><a class="login" href="#">Login</a></li>
	</ul>
<br>"""
def split_contents():
	global meta1,content1
	meta1=a2.contents[:a2.find_starting_point("total",a2.contents)+1]
	content1=a2.contents[a2.find_starting_point("total",a2.contents)+1:]
split_contents()
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
	form="""<form action="/sort"  method="GET" >Sort by
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
	meta[0][0]="Sorted by %s in %s Order "%(col_names[a],b)
	data=meta+data
	return a2.template %{'title':"Sorted by %s"%col_names[a],'navbar':navbar,'form':form,'table':a2.make_table(data)}
def search_province():
	global content1,meta1
	meta,content=deepcopy(meta1),deepcopy(content1)
	form="""<form action="/search" method="GET" class="simple-form" >
                <input size="55" type="search" placeholder="Please enter at least 2 characters. Only English characters allowed." pattern="[A-Za-z]{2,}" required name="province">
                <input type="submit" value="Search" />
             </form><br>"""
	try:
		name=request.GET['province'].lower()
	except KeyError:
		name=""
	if name =="":
		return a2.template %{'title':"Search a Province",'navbar':navbar,'table':a2.make_table(a2.contents),'form':form}
	data=[]
	for row in content:
		if name.lower() in row[0].replace('İ','i').lower().replace('ç','c').replace('ğ','g').replace('ı','i').replace('ö','o').replace('ş','s').replace('ü','u'):
			if row[0].replace('İ','i').lower().replace('ç','c').replace('ğ','g').replace('ı','i').replace('ö','o').replace('ş','s').replace('ü','u').startswith(name.lower()):
				p=row[0].replace('İ','i').lower().replace('ç','c').replace('ğ','g').replace('ı','i').replace('ö','o').replace('ş','s').replace('ü','u').partition(name.lower())
				l=list(p)
				l[1]="<b>"+l[1].title()+"</b>"
				row[0]="".join(l)
				data=[row]+data
			else:
				p=row[0].replace('İ','i').lower().replace('ç','c').replace('ğ','g').replace('ı','i').replace('ö','o').replace('ş','s').replace('ü','u').partition(name.lower())
				l=list(p)
				l[0]=l[0].title()
				l[1]="<b>"+l[1]+"</b>"
				row[0]="".join(l)
				data+=[row]
	data=meta+data
	if data==meta:
		return a2.template %{'title':"Searching Result",'navbar':navbar,'form':form,'table':"<p>No records were found that match the specified search crieteria :( <a href=\"/search\"> See full table...</a></p>"}
	a2.calculate_the_cells(data)
	data[0][0]="Provinces that include '"+name.title() +"'"
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
	cond="""
	<form action="/filterresult" class="simple-form" method="POST">
		<!--<p>Please specify filter condition(s):</p>-->
	%(name)s%(pop)s%(in)s%(out)s %(net)s%(rate)s
		<input type="submit" value="Filter">
	</form>
	"""
	di={'name':"",'pop':"",'in':"",'out':"",'net':"",'rate':""}
	for i in di.keys():
		if type(request.POST.get(i)) is str:
			di[i]="+"
	form_input="""<div class="inputs">
			<label>%(ln)s</label>
			<select name="%(name)sgl">
				<option value="g">greater than</option>
				<option value="l">less than</option>
			</select>
			<input type="number" min="0" name="%(name)s" value="0" step="1" required>
			<br>
		</div>"""
	ln={'pop':"Population",'in':"In-migration",'out':"Out-migration",'net':"Net migration",'rate':"Rate of net migration"}
	inputs={'name':"",'pop':"",'in':"",'out':"",'net':"",'rate':""}
	for i in di.keys():
		if di[i]=='+':
			if i=='name':
				inputs[i]="""	<div class="inputs">
			<label>Province name includes</label>
			<input size="45" type="search" placeholder="Only English characters are allowed." pattern="[A-Za-z]{1,}" name="name" required ><br>
			<label for="cs">Case-sensitive</label>
			<input type="checkbox" name="cs" value="enabled">
			<br>
		</div>"""
			else:
				inputs[i]=form_input%{'ln':ln[i],'name':i}
	return a2.template %{'title':"Set Filter Condition(s)",'navbar':navbar,'table':a2.make_table(a2.contents),'form':cond%inputs}

def filt_name(search,cs,data):
	new_data=[]
	
	if cs=='enabled':
		for row in data:
			tempdata=row[0]
			for i in tr_to_en.keys():
				tempdata=tempdata.replace(i,tr_to_en[i])
			if search in tempdata:
				new_data+=[row]
	else:
		for i in tr_to_en.keys():
			search=search.replace(i,tr_to_en[i])
		search=search.lower()
		for row in data:
			tempdata=row[0]
			for i in tr_to_en.keys():
				tempdata=tempdata.replace(i,tr_to_en[i])
			tempdata=tempdata.lower()
			if search in tempdata:
				new_data+=[row]
	return new_data

def filter_it(col,val,gl,data):
	if gl=='g':
		new_data=[row for row in data if row[a2.find_starting_point(col,a2.contents)]>int(val)]
	elif gl=='l':
		new_data=[row for row in data if row[a2.find_starting_point(col,a2.contents)]<int(val)]
	return new_data

def filter_result():
	global meta1,content1
	meta,content=deepcopy(meta1),deepcopy(content1)
	data=[]
	data+=content
	table_header={'name':"",'pop':"",'in':"",'out':"",'net':"",'rate':""}
	di={'name':"",'pop':"",'in':"",'out':"",'net':"",'rate':""}
	for i in di.keys():
		if type(request.POST.get(i)) is str:
			di[i]="+"
	for i in di.keys():
		if di[i]=='+':
			if i=='name':
				search=request.POST.get(i)
				cs=request.POST.get('cs')
				data=filt_name(search,cs,data)
				if cs=="enabled":
					cs="Yes"
				else:
					cs="No"
				table_header[i]="""<div class="tooltip">%s,
  <span class="tooltiptext">%s includes: '%s'<br>Case-sensitive: %s</span>
</div>"""%(col_names[i],col_names[i],search,cs)
			else:
				col=i
				val=request.POST.get(i)
				gl=request.POST.get(i+"gl")
				data=filter_it(col,val,gl,data)
				if gl=="g":
					gl="greater than"
				else:
					gl="less than"
				table_header[i]="""<div class="tooltip">%s,
  <span class="tooltiptext">%s is %s %s.</span>
</div>"""%(col_names[i],col_names[i],gl,val)
				
	if len(data)==0:
		return a2.template %{'title':"Filter Result",'navbar':navbar,'form':"",'table':"<p>No records were found that match the specified search crieteria :( <a href=\"/filter\"> See full table...</a></p>"}
	
	meta[0][0]="Filtered by: %(name)s %(pop)s %(in)s %(out)s %(net)s %(rate)s"%table_header
	data=meta+data
	a2.calculate_the_cells(data)
	return a2.template %{'title':"Filter Result",'navbar':navbar,'form':"",'table':a2.make_table(data)}
def server_static(path):
	return static_file(path, root=".")
route('/search', 'GET', search_province)
route('/', 'GET', index)
route('/sort', 'GET', sort_by_what)
route('/filter', 'GET', get_filter_criterias)
route('/set+filter+conditions', 'POST', get_filter_cond)
route('/filterresult', 'POST', filter_result)
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

