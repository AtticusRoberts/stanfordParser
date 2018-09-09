
import re 
import crawler
import copy 

disputeSearchObj = ["MID #","MID Name","Start Date","End Date","Initiator","Target","Highest Overall Act","Total Fatalities","Outcome",
				"Location"]

sourceSearchObj=['ProQuest Historical Newspapers:','Lexis-Nexis:','Facts on File:','London Times:',
				'Keesing\'s:','Narrative']

restSearchObj=['Narrative','Non-state actor involvement?','Issue Description','Authority','Disputed Facts','Ultimatums/Demands',
				'Research Notes','Articles']
data={}
mids=[]
midNums=open('midNums.txt','r')
def cleaner(datastr):
	datastr=re.sub(r'<p class=\"vspace\">','',datastr)
	datastr=re.sub(r'</span></strong> ?<br/><br/>','',datastr)
	datastr=re.sub(r"\n",'',datastr)
	datastr=re.sub(r"THIS NEEDS TO STAY COMMENTED OUT(.+)ARTICLE TITLE AND DATE HERE",'',datastr)
	datastr=re.sub(r"<br clear\=\"all\"/>","",datastr)
	return datastr

def verparse(copystr):
	tempSave ={}
	linkSave=[]
	if re.search(r'---',copystr):
		tempSave["data"]=re.sub(r"---.+",'',copystr)
		copystr = re.search(r"---.+",copystr).group()
		tempSave["ver"]=re.search(r'verified|unverified',re.sub(r"---(.+)---",'',copystr)).group()
		tempSave["inits"]=re.search(r'\(([A-Za-z]{3})',re.sub(r"---(.+)---",'',copystr)).groups(0)[0]
		tempSave["date"]=re.search(r'(\d+\-\d+\-\d+)',re.sub(r"---(.+)---",'',copystr)).groups(0)[0]
		unparsedLinks=re.sub(r'\-\-\-.+\(','',copystr).split('</a>')
		for y in range(len(unparsedLinks)-1):
			if re.search(r'href\=\"(.+)\" rel',unparsedLinks[y]):
				linkSave.append(re.search(r'href\=\"(.+)\" rel',unparsedLinks[y]).groups(0)[0])
		tempSave['links']=linkSave
		try:
			tempSave["notes"]=re.search(r'\)(.*)\(\<a class\=',re.sub(r"---(.+)---",'',copystr)).groups(0)[0]
		except AttributeError:
			tempSave["notes"]="None"
	elif re.search(r'---',copystr) == None:
		tempSave["data"]=copystr
	return tempSave

def narrativeGather(datastr):
	rest={}
	for y in range(len(restSearchObj)-1):
		data=[]
		x=re.search(restSearchObj[y]+r'(.+)'+restSearchObj[y+1],datastr).groups(0)[0].split('</p>')
		x.pop(len(x)-1)
		for i in x:
			tempSave=[]
			temp=re.split(r'\(|\)\.?',i)
			for z in temp:
				tempDict={}
				if re.search(r'href=\"(.+)\" rel',z):
					tempSave.append(re.search(r'href=\"(.+)\" rel',z).groups(0)[0])
				else:
					tempSave.append(z)
			for ab in tempSave:
				if ab==' ':
					tempSave.remove(' ')
			data.append(tempSave)
		print restSearchObj[y]+' --> '+'COLLECTED'
		rest[restSearchObj[y]]=data
	return rest

def disputeInfoGather(datastr):
	for x in range(len(disputeSearchObj)-1):
		multi=[]
		copystr=re.sub(r"^\s","",re.search(disputeSearchObj[x]+r's?'+r".?:</strong>(.*)<strong>"+disputeSearchObj[x+1]+"s?"+":",datastr).groups(0)[0])
		if re.search(disputeSearchObj[x]+r's'+r".?:</strong>(.*)<strong>"+disputeSearchObj[x+1]+"s?"+":",datastr):
			#print "Multiple "+disputeSearchObj[x]+"s"
			for i in range(len(re.split(r"[A-Z]{3} \(",copystr))):
				temp=verparse(re.split(r"[A-Z]{3} \(",copystr)[i])
				temp['data']=re.findall(r"([A-Z]{3}) \(",copystr)[i-1]
				multi.append(temp)

			multi.pop(0)

			data[disputeSearchObj[x]]=multi
		else:
			data[disputeSearchObj[x]] = verparse(copystr)
		print disputeSearchObj[x]+' --> '+'COLLECTED'
	return data

def sourceGather(datastr):
	return re.search(r'MID 2\'1 Sources',datastr)

def incidentGather(datastr):
	incidentData=[]
	data=re.search(r'(<strong>Incident:</strong>.+)<strong>MID 2.1 Sources:</strong> ',datastr).groups(0)[0].split('<strong>Incident:</strong>')
	for i in range(len(data)-1):
		incidentData.append(verparse(data[i+1]))
		print 'Incident '+str(i)+' --> '+'COLLECTED'
	return incidentData

def sourceSearchGather(datastr):
	sources={}
	
	for i in range(len(sourceSearchObj)-1):
		sources[sourceSearchObj[i]]=re.split(r's?S?earch T?t?erms',re.sub(r'<div class=\"sectionedit.+','',re.search(sourceSearchObj[i]+r'(.+)'+sourceSearchObj[i+1],datastr).groups(0)[0]))
		sources[sourceSearchObj[i]].pop(0)
	for i in sources:
		sourceList=[]
		for x in sources[i]:
			sourceSave={}
			linkSave=[]
			sourceSave['Search Terms']=re.sub(r'<br/>','',re.search(r'(.+)Dates s?S?earched',x).groups(0)[0]).split(',')
			sourceSave['Dates Searched']=re.sub(r'<br/>','',re.search(r'Dates s?S?earched:(.+)Articles f?F?iled',x).groups(0)[0])
			for y in re.search(r'A?a?rticles f?F?iled:(.+)',x).groups(0)[0].split('<a'):
				if re.search(r'href=\"(.+)\" rel',y):
					linkSave.append(re.search(r'href=\"(.+)\" rel',y).groups(0)[0])
			sourceSave['Articles filed']=linkSave
			sourceList.append(sourceSave)
		sources[i]=sourceList
		print i+' --> '+'COLLECTED'
	return sources
def twoSources(datastr):
	sources={}
	copystr=re.search(r'MID 2\.1 Sources.+Record of Sources Searched',datastr).group()
	x=re.findall(r'(([a-zA-Z0-9]+\s?)+)( --- u?n?verified (\([A-Z]+( \d+-\d+-\d+)?\))?)+',copystr)
	for i in x:
		sources[i[0]]=i[2]
	return sources

def articleGather(datastr):
	articles=[]
	string=re.search(r'Articles(.+)lastmod',re.search(r'Research Notes(.+)lastmod',datastr).group()).group()
	tempArticles=re.split(r'<a',string)
	tempArticles.pop(0)
	for i in tempArticles:
		articles.append(re.search(r'href=\"(.+)\" rel',i).groups(0)[0])
	print 'Articles --> COLLECTED'
	return articles
def gather():
	for num in midNums:
		datastr=str(crawler.crawl(num))
		
		incidentSave=[]
		data={}
		datastr=cleaner(datastr)
		
		data = disputeInfoGather(datastr)
		incidentData=incidentGather(datastr) 
		data['Sources']=sourceSearchGather(datastr)
		#data['Rest']=narrativeGather(datastr)
		stuff=narrativeGather(datastr)
		for i in stuff:
			data[i]=stuff[i]
		for i in range(len(incidentData)):
			incidentSave.append(incidentData[i])

		data['Incidents']=incidentData
		data['MID 2.1 Sources']=twoSources(datastr)
		data['Articles']=articleGather(datastr)
		#mids.append(copy.deepcopy(data))
		mids.append(data)
		print "FINISHED PARSING MID NUMBER "+num
	return mids