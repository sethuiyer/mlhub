import pickle
import pandas as pd 
from sklearn.utils import resample
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import os 

class PokemonTypeIdentifier():
    """
        This class identifies the pokemon type of a user given pokemon name.
    """
    def __init__(self):
        self.isModelLoaded = False
        self.isFileFound = False
        if os.path.isfile("models/tfidf.pickle") and os.path.isfile("models/model.pickle"):
            self.tfidf = pickle.load(open("models/tfidf.pickle","rb"))
            self.model = pickle.load(open("models/model.pickle","rb"))
            self.isModelLoaded = True
        if os.path.isfile('updated_pokemon.csv'):
            df = pd.read_csv('updated_pokemon.csv')
            category = list(dict(df['Type 1'].value_counts()).keys())
            df_majority = df[df['Type 1'] == 'Water']
            for i in range(1,len(category)):
                df_minority = df[df['Type 1'] == category[i]]
                df_minority_upsampled = resample(df_minority, 
                                            replace=True,     # sample with replacement
                                            n_samples=103,    # to match majority class
                                            random_state=123) # reproducible results
                df_majority = pd.concat([df_majority, df_minority_upsampled])
            encoded_labels,decoded_labels = pd.factorize(df_majority['Type 1'])
            self.decoded_labels = decoded_labels
            self.isFileFound = True
        if not self.isModelLoaded and self.isFileFound:
            

            self.tfidf = TfidfVectorizer(min_df=2, max_features = None, strip_accents = 'unicode', norm='l2',
                            analyzer = 'char', token_pattern = r'\w{1,}',ngram_range=(1,5),
                            use_idf = 1, smooth_idf = 1, sublinear_tf = 1, stop_words = 'english')

            features = self.tfidf.fit_transform(df_majority['Name']).toarray()
            encoded_labels,decoded_labels = pd.factorize(df_majority['Type 1'])
            self.model = LinearSVC().fit(features,encoded_labels)
            self.decoded_labels = decoded_labels
        if not self.isModelLoaded or not self.isFileFound:
            raise AttributeError("Required File Doesn't Exist.")
    def predict_type(self,poke_str):
        """
            Finds the probable Pokemon type given the user string.
            Input: A string, of which type is to be identified.
            Output: The Probable pokemon type 
        """
        return self.decoded_labels[self.model.predict(self.tfidf.transform([poke_str]))[0]]

