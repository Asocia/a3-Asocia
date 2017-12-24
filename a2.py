
import csv
contents = []
with open("a2_input.csv") as input_file:
	for row in csv.reader(input_file):
		contents = contents + [row]
#~ f=open("a2_output.html","w")
#Counts and returns number of columns
def column(contents):
	count=i=0
	while (True):
		try:
			column=contents[0][i]
			count+=1
			i+=1
		except IndexError:
			return count
#Counts and returns number of rows
def row(contents):
	count=i=0
	while (True):
		try:
			column=contents[i][0]
			count+=1
			i+=1
		except IndexError:
			return count

def find_starting_point(a,contents):
	if a == "total":
		return find_total(contents)
	elif a == "pop":
		return population(contents)
	elif a == "in":
		return in_migration(contents)
	elif a == "out":
		return out_migration(contents)
	elif a == "net":
		return find_net(contents)
	elif a == "rate":
		return find_rate(contents)
	


def find_total(contents):
	for i in range(row(contents)):
		for j in range(column(contents)):
			if contents[i][j]=="Total":
				return i

def population(contents):
	for i in range(row(contents)):
		for j in range(column(contents)):
			if contents[i][j]=="Total population":
				return j

def in_migration(contents):
	for i in range(row(contents)):
		for j in range(column(contents)):
			if contents[i][j]=="In-migration":
				return j
def out_migration(contents):
	for i in range(row(contents)):
		for j in range(column(contents)):
			if contents[i][j]=="Out-migration":
				return j

def find_net(contents):
	for i in range(row(contents)):
		for j in range(column(contents)):
			if contents[i][j]=="Net migration":
				return j

def find_rate(contents):
	for i in range(row(contents)):
		for j in range(column(contents)):
			if contents[i][j]=="Rate of net migration (&permil;)":
				return j
	
	
	
#Checks whether the row is empty
def is_row_exists(row_index,contents):
	for i in range(column(contents)):
		if contents[row_index][i]=="":
			continue
		return True
	return False
#Checks whether the cell is real number
def is_number(row_index,column_index,contents):
	try:
		float(contents[row_index][column_index])
		return True
	except ValueError:
		return False
#Converts the string to an integer or a floating number
def make_number(row_index,column_index,contents):
	try:
		contents[row_index][column_index]=int(contents[row_index][column_index])
		return False
	except ValueError:
		contents[row_index][column_index]=round(float(contents[row_index][column_index]),2)
		return True
#Converts whole page-data to their correct type.
def string_to_number(contents):
	for i in range(row(contents)):
		for j in range(column(contents)):
			if is_number(i,j,contents):
				make_number(i,j,contents)
#Does the calculations for total population, total in-migration etc...
def total(contents):
	for j in range(column(contents)):
		if is_number(find_starting_point("total",contents),j,contents):
			total=0
			for i in range(find_starting_point("total",contents)+1,row(contents)):
				if is_row_exists(i,contents):
					total+=contents[i][j]
					
			contents[find_starting_point("total",contents)][j]=total
#Does the calculations for net migrations of every provinces
def net_migration(contents):
	for i in range(find_starting_point("total",contents)+1,row(contents)):
		if is_row_exists(i,contents):
			contents[i][find_starting_point("net",contents)]=contents[i][find_starting_point("in",contents)]-contents[i][find_starting_point("out",contents)]
#Does the calculations for the rate of net migrations of every provinces
def rate_of_net(contents):
	for i in range(find_starting_point("total",contents),row(contents)):
		if is_row_exists(i,contents):
			contents[i][find_starting_point("rate",contents)]=float(contents[i][find_starting_point("net",contents)])/float(contents[i][find_starting_point("pop",contents)])*1000
			contents[i][find_starting_point("rate",contents)]=round(contents[i][find_starting_point("rate",contents)],2)
		
#Does all calculations together
def calculate_the_cells(contents):
	net_migration(contents)
	total(contents)
	rate_of_net(contents)



string_to_number(contents)
calculate_the_cells(contents)
for j in range(find_rate(contents),column(contents)):
	contents[find_total(contents)][j]= round(contents[find_total(contents)][j],2)



template="""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>%(title)s</title>
    <link rel="stylesheet" type="text/css" href="/static/stylesheet.css"/>
  </head>
  <body>
    %(navbar)s
    %(form)s
    %(table)s
  </body>
</html>
"""
def title():
	return "Turkey Population Analysis"

def make_table(contents):
	return "<table>\n"+make_row(contents)+"\n    </table>"
def make_row(contents):
	rows=""
	for i in range(row(contents)):
		if is_row_exists(i,contents):
			rows+="      <tr>\n"+make_column(i,contents)+"      </tr>\n"
	return rows
def make_column(i,contents):
	columns=""
	colspan=0
	for j in reversed(range(column(contents))):
		if contents[i][j]!="":
			if colspan==0:
				if i==0:
					if is_number(i,j,contents):
						columns="        <th class=\"title\">"+"{:,}".format(contents[i][j])+"</th>\n"+columns
					else:
						columns="        <th class=\"title\">"+str(contents[i][j])+"</th>\n"+columns
				elif i<find_starting_point("total",contents)+1:
					if is_number(i,j,contents):
						columns="        <th>"+"{:,}".format(contents[i][j])+"</th>\n"+columns
					else:
						columns="        <th>"+str(contents[i][j])+"</th>\n"+columns
				else:
					if is_number(i,j,contents):
						columns="        <td>"+"{:,}".format(contents[i][j])+"</td>\n"+columns
					else:
						columns="        <td>"+str(contents[i][j])+"</td>\n"+columns
			elif i==0:
				if is_number(i,j,contents):
					columns="        <th class=\"title\" colspan=\""+str(colspan+1)+"\">"+"{:,}".format(contents[i][j])+"</th>\n"+columns
				else:
					columns="        <th class=\"title\" colspan=\""+str(colspan+1)+"\">"+str(contents[i][j])+"</th>\n"+columns
				colspan=0
			else:
				if is_number(i,j,contents):
					columns="        <th colspan=\""+str(colspan+1)+"\">"+"{:,}".format(contents[i][j])+"</th>\n"+columns
				else:
					columns="        <th colspan=\""+str(colspan+1)+"\">"+str(contents[i][j])+"</th>\n"+columns
				colspan=0
		else:
			colspan+=1
			
			
	return columns

def number_of_cities():
	count=0
	for i in range(find_starting_point("total")+1,row()):
		if is_row_exists(i):
			count+=1
	return count
def higher_than_2M():
	count=0
	for i in range(find_starting_point("total")+1,row()):
		if is_row_exists(i) and contents[i][find_starting_point("pop")]>=2000000:
			count+=1
	return count
def lower_than_200k():
	count=0
	for i in range(find_starting_point("total")+1,row()):
		if is_row_exists(i) and contents[i][find_starting_point("pop")]<=200000:
			count+=1
	return count
def average_population():
	
	average=contents[find_starting_point("total")][find_starting_point("pop")]//number_of_cities()
	return average
def avg_over_2M():
	sum=0
	for i in range(find_starting_point("total")+1,row()):
		if is_row_exists(i) and contents[i][find_starting_point("pop")]>=2000000:
			sum+=contents[i][find_starting_point("pop")]
	average=sum//higher_than_2M()
	return average
summary_statistics="""
%s
"""
def summary_table():
	return "    <br><br>\n    <table>\n"+summary_rows()+"    </table>"
def summary_rows():
	rows=""
	for i in range(5):
		rows+="      <tr>\n"+summary_columns(i)+"      </tr>\n"
	return rows
def summary_columns(i):
	columns=""
	for j in range(2):
		columns+="        <td>%s\n        </td>\n"
	if i==0:
		return columns%("Number of Cities","{:,}".format(number_of_cities()))
	elif i==1:
		return columns%("Number of Cities with population higher than 2M","{:,}".format(higher_than_2M()))
	elif i==2:
		return columns%("Number of Cities with population lower than 200k","{:,}".format(lower_than_200k()))
	elif i==3:
		return columns%("Average population of cities","{:,}".format(average_population()))
	elif i==4:
		return columns%("Average population of cities with population over 2M","{:,}".format(avg_over_2M()))
			
#~ f.write(template %(title(contents),make_table(contents)))
#~ f.close()
#~ from webbrowser import open_new_tab
#~ open_new_tab("a2_output.html")
