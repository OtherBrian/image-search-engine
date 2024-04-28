import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import numpy as np


nltk.download('stopwords') 


class PokemonSearch():
    def __init__(self):
        self.pokemon_dict = None
        self.tokenizer =  RegexpTokenizer(r'\w+')
        self.inverted_index = None
        self.average_poke_length = None
        self.n = None
        self.pokemon_names = None


    def create_index(self, pokemon_dict):

        '''
        Takes the dictionary containing all of the Pokemon, and returns an inverted index in the form of a dictionary.
        The keys are the tokens present in the full corpus.
        The values are the list of Pokemon that each term appears in.
        '''

        self.pokemon_dict = pokemon_dict
        self.pokemon_preprocessing()
        
        inverted_index = {}
        # Iterate through the combined_content for each doc
        for pokemon in self.pokemon_dict:
            for word in self.pokemon_dict[pokemon]['text']:
                # If the word in the combined_content is in the inverted_index, add this doc number
                # Else create a new set of doc numbers using this doc number
                if word in inverted_index:
                    inverted_index[word].add(pokemon)
                else: 
                    inverted_index[word] = {pokemon}
    
        self.inverted_index = inverted_index

        self.prepare_measures()

        return self

        
    def prepare_measures(self):
        # The following two values are consistent for all Pokemon, so calculating outside of the loops.
        self.average_poke_length = sum(len(self.pokemon_dict[pokemon]['text']) for pokemon in self.pokemon_dict.keys()) / len(self.pokemon_dict)
        self.n = len(self.pokemon_dict)

        return self


    def pokemon_preprocessing(self):
        # Forgot to change to lowercase in initial pre-processing. Doing it here for now.
        counter = 0
        for pokemon in self.pokemon_dict:
            self.pokemon_dict[pokemon]['text'] = ['pokemon' if token.lower() ==  'pokémon' else token.lower() for token in self.pokemon_dict[pokemon]['text']]
            self.pokemon_dict[pokemon]['number'] = counter

            counter += 1

        return self


        
    def query_preprocessing(self, query):
    
        '''
        Tokenizes the given text and removes any stopwords.
        Returns the tokens as a list.
        '''
    
        text_tokens = self.tokenizer.tokenize(query)
        preprocessed_query = ['pokemon' if word.lower() == 'pokémon' else word.lower() for word in text_tokens if not word in stopwords.words()]
    
        return preprocessed_query

        
    def query(self, query, k=1.2, b=0.75):

        '''
        Takes a given query, the documents dictionary, and inverted index.
        Returns a list of the 100 best matched document numbers and their scores as two separate lists.
        '''

        preprocessed_query = self.query_preprocessing(query)

        # Create a vector to store the results for each Pokemon.
        results_vec = np.zeros(len(self.pokemon_dict))

        # Iterate through each doc
        for index, pokemon in enumerate(self.pokemon_dict):
            bm25_score = 0
 
            # Calculate the bm25 score for each query word for each Pokemon. 
            # The score for each word is added to the overall bm25_score for the Pokemon.
            for word in set(preprocessed_query):
                if word in self.inverted_index:
                    # Calculating the idf component.
                    n_q = len(self.inverted_index[word])
                    idf = np.log(((self.n - n_q + 0.5) / (n_q + 0.5)) + 1)
                    freq = self.pokemon_dict[pokemon]['text'].count(word)

                    # Calculating the tf component.
                    tf = (freq * (k + 1)) / (freq + k * (1 - b + b * len(self.pokemon_dict[pokemon]['text']) / self.average_poke_length))

                    # Calculate the score for the given word, and add to the Pokemon's overall score.
                    bm25_score += tf * idf

            # Store the score for the document in the results_vec array.     
            results_vec[index] = bm25_score

        # Get the 25 docs with the highest bm25 score in descending order
        most_similar_pokemon_index = np.argsort(results_vec,-1)[::-1][:25]


        # Getting the names of each Pokemon in another vector to indexing later.
        self.pokemon_names = [pokemon for pokemon in self.pokemon_dict]
        pokemon_names = list(np.array(self.pokemon_names)[most_similar_pokemon_index])

        return dict([(pokemon, self.pokemon_dict[pokemon]['image']) for pokemon in pokemon_names])

