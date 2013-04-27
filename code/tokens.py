## IMPORTING NECESAARY FILES

import pickle # Loading Pickle attribute and relation file
import re # Regular Expression for getting movie token e.g. "Titanic"
import nltk 
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet as wn # For Synsets
from nltk.stem.wordnet import WordNetLemmatizer 
from nltk.stem.lancaster import LancasterStemmer
from stemming.porter2 import stem as stemmer
from attach import * # Maxflow algorithm

#Relation Synonyms
relation = {'actor':[],
            'director':[],
            'movie':[]}
#Attribute Synonyms
attribute = {'name':[],
             'gender':[],
             'year':[],
             'rank':[]}
#Database Structure
db_struct = {'actor':['name','gender'],
             'movie':['name','year','rank'],
             'director':['name']
             }
#Wh association on the relation
wh_struct = {'when':{'movie':['year'],
                     'director':None,
                     'actor':None},
             'what':{'movie':['name'],
                     'director':['name'],
                     'actor':['name']},
             'who':{'movie':None,
                    'director':['name'],
                    'actor':['name']},
             'where':{'movie':None,
                      'director':None,
                      'actor':None},
             'which':{'movie':['name'],
                      'director':['name'],
                      'actor':['name']}
             }

#Stores query
query=''
#Stores tokens of query
word_tokens=[]


#Preparing relation synset
def prep_rel():
    for elem in relation.keys():
        filein = open('rel_'+elem,'r')
        relation[elem] = pickle.load(filein)

#Preparing attribute synset
def prep_atr():
    for elem in attribute.keys():
        filein =open('atr_'+elem,'r')
        attribute[elem] = pickle.load(filein)


#Finds Movie names and return query-movie_names and movie_names
def movie_name(text):
    pattern = '\"[^(\")]*\"'
    movie_names = re.findall(pattern,text)
    for name in movie_names:
        text = text.replace(name,"")
    return text,movie_names
#Finds person names and returns query-person and person_names 
def getNamedEntity(text):
    ret=[]
    for sent in nltk.sent_tokenize(text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'node') and chunk.node=='PERSON':
                 ret.append(' '.join([c[0] for c in chunk.leaves()]))

    for elem in ret:
        text = text.replace(elem,"")
    return text,ret

#Finds Year and returns query-year and year
def getYearToken(text):
    tokenizer = RegexpTokenizer("[12][0-9][0-9][0-9]|(\'[0-9][0-9])")
    ret_tokens=[]
    for t in tokenizer.tokenize(text): # '94 is 1994 and '04 is 2004
        if "\'" in t:
            try:
                text=text.replace(t,"")
                s = t.replace("\'","")
                if int(s)>12 and int(s)<100:
                    s='19'+s
                else:
                    s='20'+s
                ret_tokens.append(s)                
            except:
                print 'Error in tokenizing year' + t
        else:
            ret_tokens.append(t)
    return text,ret_tokens    

#Returns the dbelement for a token
def detect(word):
    for key in relation:
        sets=relation[key]
        for every_set in sets:
            if word in every_set:
                return [key]

    for key in attribute:
        sets=attribute[key]
        for every_set in sets:
            if word in every_set:
                rltns=get_relations(key)
                ret=[]
                for rltn in rltns:
                    ret.append(rltn+"."+key)
                return ret
    return None


#Gives relation set for given attribute
def get_relations(attrb):
    ret=[]
    for key in db_struct:
        if attrb in db_struct[key]:
            ret.append(key)
    return ret


#Finding rest of the tokens
def tokenize_rest(text):
    wnl =  WordNetLemmatizer()
    st = LancasterStemmer()
    words = nltk.word_tokenize(text)
    postag = nltk.pos_tag(words)
    
    tokens = []
    whfound=False
    for word in words:
        if word[0:2].lower() == 'wh' and not whfound:
            tokens.append({word.lower():'wh'})
            whfound = True
            continue
        elem=wnl.lemmatize(word)
        stem = st.stem(elem)
        synd = wn.synsets(stem)
        if not synd:
            stem = stemmer(elem)
            synd = wn.synsets(stem)
        if not synd:
            stem = elem
            synd = wn.synsets(stem)
        dbelement=detect(stem)
        if dbelement:
            for every_elem in dbelement:
                tokens.append({word:every_elem})
    print "\n Rest of possible Tokens"
    print tokens
    return tokens


#################################################################
#Restricting rests of possible tokens
def restrict_rests(rest):
    ## Restricting Rest
    new_rest=[]
    for token in rest:
        for key in token.keys():
            if token[key].find('.')==-1:
                new_rest.append(token)
    
    for token in rest:
        for key in token.keys():
            if token[key].find('.')!=-1:
                rel,attrb=token[key].split('.')
                if inRests(new_rest,rel):
                    new_rest.append(token)
    rest=new_rest
    return rest

# Present in ret tuple
def inRests(new_rest, rel):
    for token in new_rest:
        for key in token.keys():
            if rel in token[key]:
                return True
    return False

###################################################
def associate_wh(wh, lookinto):
    whindex=0
    for word in word_tokens:
        if word.lower() in wh.keys():
            whindex = word_tokens.index(word)
            break;
    word = word_tokens[whindex].lower()
    for wtkn in word_tokens:
        if present(lookinto,wtkn) != None:
            wh[word] = present(lookinto,wtkn)
            break


    if wh[word].find('.')!=-1:
        return [wh]
    else:
        new_wh=[]
        wh_dict=wh_struct[word]
        wh_list=wh_dict[wh[word]]
        for elem in wh_list:
            new_wh.append({word:wh[word]+'.'+elem})
        return new_wh
    return None

#Check if present in the keys
def present(lookinto, key):
    for elem in lookinto:
        if key in elem.keys():
            return elem[key]
    return None

####################################################
def finalize(movie, person, year, rest):
    final_max_flow_list=[]
    rest=restrict_rests(rest)
    print "\n Restricting tokens"
    print rest
    print "\n Associating wh token"
    rest=associate_wh(rest[0],rest[1:])+rest[1:]
    print rest
    for elem in rest:
        for key in elem.keys():
            if key[:2]=='wh':
                final_max_flow_list.append({'token':key,'dbelement':key,'use':elem[key],'explicit':isExplicit(elem[key],rest,key),'attribute':elem[key]})

    ##TAKING CARE OF MOVIES
    if movie != None:
        for mv in movie:
            final_max_flow_list.append({'token':mv,'dbelement':mv,'use':'movie.name','explicit':isExplicit('movie.name',rest,'mv'),'attribute':'movie.name'})

    ##TAKING CARE OF YEAR
    if year!=None:
        for yr in year:
            final_max_flow_list.append({'token':yr,'dbelement':yr,'use':'movie.year','explicit':isExplicit('movie.year',rest,'yr'),'attribute':'movie.year'})
    ##TAKING CARE OF PERSONS
    if person!=None:
        for head in person:
            rel = act_direct(head)
            final_max_flow_list.append({'token':head,'dbelement':head,'use':rel+'.name','explicit':isExplicit(rel+'.name',rest,rel[:2]),'attribute':rel+'.name'})
    print "\n Max Flow Input"
    print final_max_flow_list
    print "\n Query attribute value pair"
    return attach(final_max_flow_list),rest

#######################################################
## Finding actor and Director Logic

def act_direct(head):
    actor = canbeactor(head)
    director = canbedirector(head)
    if actor != director:
        if actor:
            return 'actor'
        if director:
            return 'director'
    else:
        return checkwith(head)


def checkwith(head):
    send =False
    sendvalue=''
    for word in word_tokens:
        if word[:3]=='act':
            sendvalue='actor'
            
        if word[:6]=='direct':
            sendvalue='director'

        if word=='with':
            send = True
    if send:
        return sendvalue
    else:
        for word in word_tokens:
            if word[:2]=='ha':
                return 'actor'
        return 'director'


def canbeactor(head):
    prev=''
    for word in word_tokens:
        if word[:3]=='act':
            if prev[:2] != 'wh':
                return True 
        prev = word
    return False

def canbedirector(head):
    prev=''
    for word in word_tokens:
        if word[:6]=='direct':
            if prev[:2].lower() != 'wh':
                return True
        prev = word
    return False

########################################################
    
def isExplicit(value, inlist,inkey):
    for values in inlist:
        for key in values.keys():
            if value in values[key] and inkey!=key:
                return True
    return False

def formQuery(attach_it,rest):
    select = []
    db = []
    for key in rest[0].keys():
        for elem in attach_it[:]:
            if key in elem:
                select = elem.split('=')[0]
                # Fixing name into first_name+last_name
                if select in ['director.name','actor.name']:
                    person = select.split(".")[0]
                    select= 'CONCAT(%s.first_name, 0x20, %s.last_name)' % (person,person)
                attach_it.remove(elem)
    for elem in rest[1:]:
        for key in elem.keys():
            if elem[key].find('.')==-1:
                db.append(elem[key])

    for elem in attach_it:
        rel = elem.split('.')[0]
        if rel not in db:
            db.append(rel)
##    Taking Care of Joins
    if set(['actor','director','movie']) - set(db) == set([]):
        db += ['role','movie_director']
        attach_it += ['actor.id=role.actor_id',
                      'director.id=movie_director.director_id',
                      'role.movie_id=movie.id',
                      'movie.id=movie_director.movie_id']
    elif set(['actor','director']) - set(db) ==  set([]):
        db += ['role','movie_director']
        attach_it += ['actor.id=role.actor_id',
                      'director.id=movie_director.director_id',
                      'role.movie_id=movie_director.movie_id']
    elif set(['actor','movie']) - set(db) == set([]):
        db +=['role']
        attach_it += ['actor.id=role.actor_id',
                      'role.movie_id=movie.id']
    elif set(['director','movie']) - set(db) == set([]):
        db += ['movie_director']
        attach_it += ['director.id=movie_director.director_id',
                      'movie.id=movie_director.movie_id']
    print "\n Select Attribute"
    print select
    print "\n Relations it deals with"
    print db
    print "\n Attribute and Values "
    print attach_it

    query = 'select ' + select + ' from '
    for elem in db:
        if elem == db[-1]:
            query += elem + ' where '
        else:
            query += elem + ', '

    for elem in attach_it:
        # Hard coding... dangerous but karna padega for time being
        if ('director.name' in elem) or ('actor.name' in elem):
            name = elem.split("=")[1]
            spleet = name.split(" ")
            if len(spleet)>1:
                fname = spleet[0]
                lname = spleet[-1]
                if 'director' in elem:
                    elem = " (director.first_name='%s' and director.last_name='%s') " % (fname,lname)
                elif 'actor' in elem:
                    elem = " (actor.first_name='%s' and actor.last_name='%s') " % (fname,lname)
            else :
                if 'director' in elem:
                    elem = " (director.first_name='%s' or director.last_name='%s') " % (name,name)
                elif 'actor' in elem:
                    elem = " (actor.first_name='%s' or actor.last_name='%s') " % (name,name)
                
            
        if elem == attach_it[-1]:
            query += elem + ''
        else:
            query += elem + ' and '
    return query


###############################################################
##Full Conversion

def convert(question):
    global word_tokens
    global query
    prep_rel()
    prep_atr()
    query = question
    print "\n Query:"
    print query
    word_tokens=nltk.word_tokenize(query)
    womovie,movie = movie_name(query)
    woper,person = getNamedEntity(womovie)
    woyear,year = getYearToken(woper)
    print "\n Movie Person Year Tokens"
    print movie,person,year
    rest=tokenize_rest(woyear)
    attach_it,rest_list = finalize(movie,person,year,rest)
    print '\n Final query' 
    return {"query":formQuery(attach_it,rest_list),
            "attach":attach_it,
            "rest":rest_list}

def main():
    query = 'Which movies were made in the year 2000?'
##    query = 'Which movies have James Franco as actor?'
##    query = 'who directed movies having James Franco ?'
    ##query = 'Who directed the movie named "the titanic"?'
    convert(query)
    
if __name__=="__main__":main()
