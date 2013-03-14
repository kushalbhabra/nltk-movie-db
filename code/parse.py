## Placing MALT parser

import nltk
import os
print os.getcwd()
os.environ["MALTPARSERHOME"] = os.getcwd()+"\maltparser-1.7.2\\maltparser-1.7.2.jar"
query = 'Which movies have actors James and Lilly'
parser = nltk.parse.malt.MaltParser(mco = 'engmalt.linear-1.7',
                                    working_dir = 'C:\Users\DHAVAL\Documents\GitHub\nltk-movie-db\code\maltparser-1.7.2')
print parser.parse(query)
