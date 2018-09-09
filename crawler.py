import bs4 as bs
import mechanize
import re
char=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v',
		'w','x','y','z','0','1','2','3','4','5','6','7','8','9']
places=['Main.MIDs0000-0999','Main.MIDs1000-1999','Main.MIDs2000-2999','Main.MIDs3000-3999','Main.MIDs4000']
encPassword=[987350,3405980,336179,70225]
pubKey=5592901
def decrypt():
	password=''
	numText=''
	privKey=int(raw_input("Enter the private key to decrypt the password: "))
	print "DECRYPTING... (this may take a few minutes, depending on your computer)","\n"
	for i in range(len(encPassword)):
		print 'DECRYPTING CIPHER #'+str(i+1)+'...'
		numText+=str((encPassword[i]**privKey)%pubKey)
		print 'DONE'
	for i in range(len(numText)/2):
		try:
			password+=char[int(numText[i*2:i*2+2])-11]
		except IndexError:
			print 'INCORRECT KEY'
			password=''
			test='yeet'
			break
	print password
	print test
	return password
def crawl(place):
	password=decrypt()
	print "REQUESTING MID NUMBER",place[4:]
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.set_handle_refresh(False)
	url = 'http://web.stanford.edu/group/tomzgroup/cgi-bin/pmwiki/index.php?n='+str(place)
	response = br.open(url)
	br.select_form('authform')
	searchForm = list(br.forms())[0]
	authForm = list(br.forms())[1]
	passwordControl = br.form.controls[0]
	submitControl = br.form.controls[1]
	passwordControl.value = password
	response = br.submit()
	data = response.read()
	print 'DATA GATHERED, PARSING...'
	return str(bs.BeautifulSoup(data, 'lxml'))
def numGather():
	for x in range(5):
		data=crawl(places[x])
		file=open("midNums.txt","a")
		for i in re.findall(r"ID\.MID\-(.{4})\"",data):
			file.write('MID.MID-'+i+'\n')
		file.close()