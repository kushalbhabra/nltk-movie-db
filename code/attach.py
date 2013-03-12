"""
This is attachment function
"""

from FlowGraph import *

def attach(tokenset):
    g=FlowNetwork()
    values=[]
    attributes=[]
    explicit=[]
    for token in tokenset:
        if token['token'] not in values:
            values.append(token['token'])
        if token['attribute'] not in attributes:
            attributes.append(token['attribute'])
        if token['explicit']==True and token['attribute'] not in explicit:
            explicit.append(token['attribute'])

    count_explicit=len(explicit)
    count_implicit=len(values)-count_explicit
    db_values=[]
##Forming a vertex list
    vertex_list=['s']
    for elem in values:
        vertex_list.append(elem)
    for elem in tokenset:
        elem_ins=elem['attribute']+'='+elem['dbelement']
        db_values.append(elem_ins)
        vertex_list.append(elem_ins)
    for elem in attributes:
        vertex_list.append(elem)
    for elem in attributes:
        vertex_list.append('N'+elem)
    vertex_list.append('e')
    vertex_list.append('i')
    vertex_list.append('t')

##Adding Vertices    
    map(g.add_vertex,vertex_list)

##Adding edges to flonetwork
##S to VALUE TOKESN
    for elem in values:
        g.add_edge('s',elem,1)
##Value Token to DB-Value
    for elem in values:
        for db_val in db_values:
            if elem in db_val:
                g.add_edge(elem,db_val,1)
##DB-Value to DB-Attribute 1
    for elem in attributes:
        for db_val in db_values:
            if elem in db_val:
                g.add_edge(db_val,elem,1)
##DB-Attrubute 1 to DB-Attribute 2
    for elem in attributes:
        g.add_edge(elem,"N"+elem,1)
##DB-Attribute 2 to Explicit E
    for elem in explicit:
        g.add_edge("N"+elem,'e',1)
##DB-Attribute 2 to Implicit I
    implicit=list(set(attributes)-set(explicit))
    for elem in implicit:
        g.add_edge("N"+elem,'i',1)
##E to T
    g.add_edge('e','t',count_explicit)    
##I to T
    g.add_edge('i','t',count_implicit)    
    g.max_flow('s','t')
    g.set_path('s','t','')
    paths=g.get_path()
    ret=[]
    for path in paths:
        elements=path.split(' -> ')
        attr,value=elements[2].split('=')
        for token in tokenset:
            if (attr in token.values()) and (value in token.values()):
                ret.append(token['use']+'='+value)

    return ret

    


def main():
##    print "main"
##    tokenset=[{'token':'what','dbelement':'what','attribute':'desciption','explicit':False,'use':'Jobs.description'},
##              {'token':'what','dbelement':'what','attribute':'platform','explicit':True,'use':'Jobs.platform'},
##              {'token':'what','dbelement':'what','attribute':'company','explicit':False,'use':'Jobs.company'},
##              {'token':'HP','dbelement':'HP','attribute':'platform','explicit':True,'use':'Jobs.platform'},
##              {'token':'HP','dbelement':'HP','attribute':'company','explicit':False,'use':'Jobs.company'},
##              {'token':'unix','dbelement':'unix','attribute':'platform','explicit':True,'use':'Jobs.platform'}]
    tokenset = [{'attribute': 'director.name', 'token': 'who', 'explicit': False, 'use': 'director.name', 'dbelement': 'who'},
                {'attribute': 'movie.name', 'token': '"The Titanic"', 'explicit': False, 'use': 'movie.name', 'dbelement': '"The Titanic"'}]
    attach(tokenset)


if __name__ == "__main__":main()
