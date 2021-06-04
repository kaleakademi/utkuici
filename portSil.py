import sqlite3
while 1:
	conn=sqlite3.connect('port.db')
	c = conn.cursor()
	c.execute('SELECT * FROM portlar');
	bilgiler=c.fetchall()
	bilgiListe=[]
	for i in bilgiler:
		print str(i)
	conn.close()
	silinecekIP=raw_input("Silinecek IP:")
	silinecekPort=raw_input("Silinecek Port:")
	conn=sqlite3.connect('port.db')
	c = conn.cursor()
	c.execute('DELETE FROM portlar WHERE port=? and  ip=?', (silinecekPort,silinecekIP,));
	conn.commit()
	conn.close()


