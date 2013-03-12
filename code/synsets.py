from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
import pickle
from stemming.porter2 import stem as stemmer


relation = ['actor','director', 'movie']
attribute = ['name','gender','year','rank']

def relationfunction():
    wnl =  WordNetLemmatizer()
    st = LancasterStemmer()
    for elem in relation:
        final=[]
        fileop = open('rel_'+elem,'w')
        stem = st.stem(elem)
        synd = wn.synsets(stem)
        if not synd:
            stem = stemmer(elem)
            synd = wn.synsets(stem)
        if not synd:
            stem = wnl.lemmatize(elem)
            synd = wn.synsets(stem)
        for synset in synd:
            final.append(synset.lemma_names)
        pickle.dump(final,fileop)
        fileop.close()

def attributefunction():
    wnl =  WordNetLemmatizer()
    st = LancasterStemmer()
    for elem in attribute:
        final=[]
        fileop = open('atr_'+elem,'w')
        stem = st.stem(elem)
        synd = wn.synsets(stem)
        if not synd:
            stem = stemmer(elem)
            synd = wn.synsets(stem)
        if not synd:
            stem = wnl.lemmatize(elem)
            synd = wn.synsets(stem)
        for synset in synd:
            final.append(synset.lemma_names)
        pickle.dump(final,fileop)
        fileop.close()
def main():
    relationfunction()
    attributefunction()


if __name__=="__main__":main()
