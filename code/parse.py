## Placing MALT parser

import nltk
import os

os.environ["MALTPARSERHOME"] = "C:/Users/DHAVAL/Dropbox/BE_project/CODE/Syncing/maltparser-1.7.2/maltparser-1.7.2.jar"
query = 'Which movies have actors James and Lilly'
parser = nltk.parse.malt.MaltParser(mco = 'engmalt.linear-1.7')
print parser.parse(query)
