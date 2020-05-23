import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
nltk.download('wordnet')      #download if using this module for the first time


from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
nltk.download('stopwords')    #download if using this module for the first time


#For Gensim
import gensim
import string
from gensim import corpora
from gensim.corpora.dictionary import Dictionary
from nltk.tokenize import word_tokenize

# read article for refrence https://www.pluralsight.com/guides/topic-identification-nlp
def extract_topic(data,num_topics=2,num_words=5):
    compileddoc = data.split('\n')
    stopword = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()

    def clean(document):
        stopwordremoval = " ".join([i for i in document.lower().split() if i not in stopword])
        punctuationremoval = ''.join(ch for ch in stopwordremoval if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punctuationremoval.split())
        return normalized

    final_doc = [clean(document).split() for document in compileddoc]
    dictionary = corpora.Dictionary(final_doc)
    DT_matrix = [dictionary.doc2bow(doc) for doc in final_doc]
    Lda_object = gensim.models.ldamodel.LdaModel
    lda_model_1 = Lda_object(DT_matrix, num_topics=num_topics, id2word = dictionary)

    return lda_model_1.print_topics(num_topics=num_topics, num_words=num_words)