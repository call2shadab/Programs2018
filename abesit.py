import requests
from bs4 import BeautifulSoup
import mechanize
import getpass
import os

br = mechanize.Browser()
br.open('http://117.55.242.132/moodle/login/index.php')

res = br.response()



def select_form(form):
	return form.attrs.get('id',None)=='login'

br.select_form(predicate=select_form)

username = raw_input("Enter Username: ")                                 #enter moodle ID
password = getpass.getpass("Enter Your Password: ")                      #enter moodle PassWord

br.form['username'] = username
br.form['password'] = password

page = br.submit()

soup = BeautifulSoup(page.read(),'html.parser')

h2 = soup.find_all('h2',{'class':'title'})
i = 1
subjectlink = []
subjectlist = []
for items in h2:
	for atags in items.find_all('a'):
		print i, ':', atags.text
		subjectlink.append(atags.get('href'))
		subjectlist.append(atags.text)
		i+=1
subnum = input('Please select subject: ')
os.chdir('<yourpath>')                                                    #Path to create folder of selected subject
newpath = os.getcwd()+'/'+subjectlist[subnum-1]
if not os.path.exists(newpath):
	os.makedirs(newpath)
os.chdir(newpath)
print os.getcwd()
page = br.open(subjectlink[subnum-1])
soup = BeautifulSoup(page.read(),'html.parser')

div = soup.find_all('div',{'class':'activityinstance'})

for item in div:
	for atags in item.find_all('a'):
		if 'File' in atags.text:
			print 'downloading', atags.text, 'file.....' 
			p = br.open(atags.get('href'))
			f = open(atags.text+'.pdf','wb')
			f.write(p.read())
			f.close()

		elif 'Folder' in atags.text:
			newp = br.open(atags.get('href'))
			newsoup = BeautifulSoup(newp.read(),'html.parser')
			newspan = newsoup.find_all('span',{'class':'fp-filename-icon'})
			for newitem in newspan:
				for at in newitem.find_all('a'):
					new1p = br.open(at.get('href'))
					if 'pdf' not in at.text:
						f = open(at.text+'.pdf','wb')
					else:
						f = open(at.text,'wb')

					f.write(new1p.read())
					f.close()

		
					
