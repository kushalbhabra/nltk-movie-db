import MySQLdb
def dbConnect():
    conn = MySQLdb.connect (host = "localhost", user = "root", passwd = "msdhoni", db = "imdb")
    return conn

def verifyPersonWithDb(pTokens):
    # Database connection
    ret_tokens=[]
    conn = dbConnect()
    cursorActor = conn.cursor()
    cursorDirector = conn.cursor()
    for p in pTokens:
        p = p['value'].title()
        s = p.split(' ')
        if len(s)==3:
            s=[' '.join(s[0:2]),s[2]]
        if len(s)==2: # Nicholas Cage
            cursorActor.execute("SELECT * FROM actors WHERE first_name = %s AND last_name = %s", (s[0],s[1]))
            cursorDirector.execute("SELECT * FROM directors WHERE first_name = %s AND last_name = %s", (s[0],s[1]))
        else: # Nicholas
            cursorActor.execute("SELECT * FROM actors WHERE first_name = %s OR last_name = %s", (s[0],s[0]))
            cursorDirector.execute("SELECT * FROM directors WHERE first_name = %s OR last_name = %s", (s[0],s[0]))
        rowsActor=cursorActor.fetchall()
        if rowsActor!=():
            token = {'token':p,'dbelement':' '.join(s),'attribute':'actorname','explicit':True}
            ret_tokens.append(token)
        rowsDirector=cursorDirector.fetchall()
        if rowsDirector!=():
            token = {'token':p,'dbelement':' '.join(s),'attribute':'directorname','explicit':True}
            ret_tokens.append(token)
            
    conn.close()
    return ret_tokens

verifyPersonWithDb(['James Franco'])
