import requests
import sqlite3
import subprocess
import datetime
import socket
SIEMhost="127.0.0.1"
SIEMport=515
accessKey=""
secretKey=""
IP="127.0.0.1"
xapikeys="accessKey="+accessKey+"; secretKey="+secretKey+";"
header={'X-ApiKeys':xapikeys}
url="https://"+IP+":8834/scans"
sonuc=requests.get(url=url,headers=header,verify=False)
taramaIDListe=[]
ilkTaramaIPListe=[]
cikti=subprocess.check_output("ls",shell=True)
if not "hostDiscovery.db" in cikti:
	conn = sqlite3.connect('hostDiscovery.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE hosts
             (ip text, zaman text)''')
	c.close()
conn=sqlite3.connect('hostDiscovery.db')
c = conn.cursor()
c.execute('SELECT ip FROM hosts');
ipler=c.fetchall()
iplerListe=[]
for i in ipler:
	iplerListe.append(str(i[0]))
conn.close()
for i in sonuc.json()['scans']:
	if "Host Discovery" in i['name'] and "completed" in i['status']:
		url="https://"+IP+":8834/scans/"+str(i['id'])
		sonuc=requests.get(url=url,headers=header,verify=False)
		for j in  sonuc.json()['hosts']:
			if not j['hostname'] in iplerListe:
				conn=sqlite3.connect('hostDiscovery.db')
				c=conn.cursor()
				c.execute('INSERT INTO hosts VALUES (?,?)',(str(j['hostname']),str(datetime.datetime.now())))
				conn.commit()
				conn.close()
				print "Yeni Gelen IP:",j['hostname']
        			s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        			s.connect((SIEMhost,SIEMport))
        			gonderilecekMesaj="Yeni bir host bulundu:"+j['hostname']
				s.sendall(gonderilecekMesaj)
        			s.close()
