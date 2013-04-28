import MySQLdb
def dbConnect():
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "msdhoni", db = "imdb")
    return conn

def verifyPersonWithDb(p):
    # Database connection
    ret_tokens=[]
    conn = dbConnect()
    cursorActor = conn.cursor()
    cursorDirector = conn.cursor()

    s = p.split(' ')
    if len(s)==3:
        s=[' '.join(s[0:2]),s[2]]
    if len(s)==2: # Nicholas Cage
        cursorActor.execute("SELECT * FROM actor WHERE first_name = %s AND last_name = %s", (s[0],s[1]))
        cursorDirector.execute("SELECT * FROM director WHERE first_name = %s AND last_name = %s", (s[0],s[1]))
    else: # Nicholas
        cursorActor.execute("SELECT * FROM actor WHERE first_name = %s OR last_name = %s", (s[0],s[0]))
        cursorDirector.execute("SELECT * FROM director WHERE first_name = %s OR last_name = %s", (s[0],s[0]))
    rowsActor=cursorActor.fetchall()
    if rowsActor!=():
        ret_tokens.append('actor')
    rowsDirector=cursorDirector.fetchall()
    if rowsDirector!=():
        ret_tokens.append('director')
            
    conn.close()
    if ret_tokens:
        return ret_tokens
    else:
        print "No one in database"

verifyPersonWithDb('James Franco')
