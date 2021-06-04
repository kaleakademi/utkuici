import sqlite3
while 1:
	conn=sqlite3.connect('hostDiscovery.db')
	c = conn.cursor()
	c.execute('SELECT ip FROM hosts');
	ipler=c.fetchall()
	iplerListe=[]
	for i in ipler:
		print str(i[0])
	conn.close()
	silinecekIP=raw_input("Silinecek IP:")
	conn=sqlite3.connect('hostDiscovery.db')
	c = conn.cursor()
	c.execute('DELETE FROM hosts WHERE ip=?', (silinecekIP,));
	conn.commit()
	conn.close()


