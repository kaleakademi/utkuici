import requests
import sqlite3
import subprocess
import datetime
import socket
SIEMhost="127.0.0.1"
SIEMport=515
cikti=subprocess.check_output("ls",shell=True)
if not "port.db" in cikti:
	conn = sqlite3.connect('port.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE portlar
             (port text, IP text,zaman text)''')
	c.close()
accessKey=""
secretKey=""
IP="127.0.0.1"
xapikeys="accessKey="+accessKey+"; secretKey="+secretKey+";"
header={'X-ApiKeys':xapikeys}
url="https://"+IP+":8834/scans"
sonuc=requests.get(url=url,headers=header,verify=False)
for i in sonuc.json()['scans']:
	url="https://"+IP+":8834/scans/"+str(i['id'])
	sonucTarama=requests.get(url=url,headers=header,verify=False)
	for j in  sonucTarama.json()['hosts']:
		#print j
		try:
			url="https://"+IP+":8834/scans/"+str(i['id'])+"/hosts/"+str(j['host_id'])+"/plugins/14272"
			IPSonuc=requests.get(url=url,headers=header,verify=False)
			for k in IPSonuc.json()['outputs']:
				print k['ports'].keys()[0]
				print j['hostname']
				conn=sqlite3.connect('port.db')
				c=conn.cursor()
				Portkontrol=c.execute('select * from portlar where port=? and IP=?',(str(k['ports'].keys()[0]),str(j['hostname'])))
				PortSayisi=len(Portkontrol.fetchall())
				conn.close()
				if PortSayisi<1:
					log="Yeni Port:"+str(k['ports'].keys()[0])+"|"+str(j['hostname'])+"|"+str(datetime.datetime.now())+"\n"
					conn=sqlite3.connect('port.db')
					c=conn.cursor()
					c.execute('INSERT INTO portlar VALUES (?,?,?)',(str(k['ports'].keys()[0]),str(j['hostname']),str(datetime.datetime.now())))
					conn.commit()
					conn.close()
        				s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        				s.connect((SIEMhost,SIEMport))
					s.sendall(log)
        				s.close()
		except:
			pass
