__author__='Xplore'

import mechanize
from bs4 import BeautifulSoup
import urllib2, urllib
import cookielib
from lxml import *
import requests
import os
import time
import getpass


cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)

count = 1
#---- READ the FORMS ----#
'''
for form in br.forms():
    print "Form name:", form.name
    print form
'''
def encoder(str):
    str = str.encode('base64','strict')
    return str

def decoder(str):
    str = str.decode('base64','strict')
    return str

def creds():
    user = str(raw_input("Enter User id only:"))
    user = user+"@kiit.ac.in"
    print user
    passwd= str(getpass.getpass('Enter 4 digit Password:'))
    urlkey= str(raw_input("Enter key:"))
    urlkey = "https://maker.ifttt.com/trigger/new_notice/with/key/"+urlkey
    print urlkey
    #urlkey= encoder(urlkey)
    user = encoder(user)
    passwd = encoder(passwd)
    with open('creds.txt', 'w') as f:
        f.writelines([user, passwd, urlkey])
        f.close()        


def notices(user,passwd):
    br.open("http://kiittnp.in/tnp/usr/index.php")
    br.select_form(nr=0)
    br.form['user_name'] = user
    br.form['password'] = passwd
    br.submit()
    resp = br.response().read()
    soup = BeautifulSoup(resp, "lxml")    
    s = str(soup.findAll('a')[1])
    #print s[22:26]
    notice_new = int(s[22:26])
    return notice_new


def run(notice_new,notice,urlkey):
    if(notice_new > int(notice)):
        print "There is new notice -- "                            
        for i in range(int(notice)+1,notice_new+1):
            link = "http://kiittnp.in/tnp/img/notice"+str(i)+".pdf"
            print "notice"+str(i)
            filename = os.path.join('notices','notice'+str(i)+'.pdf')
            urllib.urlretrieve(link, filename)
        data = urllib.urlencode({"value1":str(notice_new - int(notice))})
        urllib.urlopen(urlkey,data)
        f = open('notice.txt', 'w')
        f.write(str(notice_new))
        f.close()                
    else:
        print "There is no new notice"
             
while(True):        
    if(os.path.isfile('./notice.txt')==True and os.path.isfile('./creds.txt')==True and os.path.isdir('./notices')==True):
        nt = open('notice.txt')
        notice = nt.read()
        with open('creds.txt', 'r') as f:
            lines = f.readlines()
            if(lines[0]!=''):                
                usertmp = lines[0]
                passtmp = lines[1]
                urltmp = lines[2]
            else:
                creds()                
                usertmp = lines[0]
                passtmp = lines[1]
                urltmp = lines[2]
        usertmp = str(decoder(usertmp))
        passtmp = str(decoder(passtmp))
        #urltmp = str(decoder(urltmp))
        notice_new = int(notices(usertmp,passtmp))
        if(notice!=''):
            run(notice_new,notice,urltmp)
            print "END ---------------"+str(count)+"--------------- END"
            print "Sleeping zzzzzzzzz"
            count = count+1
            time.sleep(900)    
        else:
            f = open('notice.txt', 'w')
            f.write(str(notice_new))
            f.close()
            

    elif(os.path.isfile('./creds.txt')==False):
        creds()
       
    elif(os.path.isdir('./notices')==False):
        os.makedirs('notices')
        
    elif(os.path.isfile('./notice.txt')==False):
        with open('creds.txt', 'r') as f:
            lines = f.readlines()
            usertmp = lines[0]
            passtmp = lines[1]            
        usertmp = str(decoder(usertmp))
        passtmp = str(decoder(passtmp))        
        notice_new = int(notices(usertmp,passtmp))
        f = open('notice.txt', 'w')
        f.write(str(notice_new))
        f.close()
        
    else:
        break
    
    


