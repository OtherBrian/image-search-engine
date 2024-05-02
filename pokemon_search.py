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

        # Iterate through the text for each Pokemon
        for pokemon in self.pokemon_dict:
            for word in self.pokemon_dict[pokemon]['text']:
                # If the word in the text is in the inverted_index, add this Pokemon man
                # Else create a new set of Pokemon names using this Pokemon name
                if word in inverted_index:
                    inverted_index[word].add(pokemon)
                else: 
                    inverted_index[word] = {pokemon}
    
        self.inverted_index = inverted_index

        self.prepare_measures()

        return self

        
    def prepare_measures(self):
        '''
        Calculates the average document length, and the total number of Pokemon.
        These will be used for the BM25 calculation later, and are the same for all queries.
        '''

        # The following two values are consistent for all Pokemon, so calculating outside of the loops.
        self.average_poke_length = sum(len(self.pokemon_dict[pokemon]['text']) for pokemon in self.pokemon_dict.keys()) / len(self.pokemon_dict)
        self.n = len(self.pokemon_dict)

        return self


    def pokemon_preprocessing(self):
        '''
        Performs additional pre-processing on the tokenized text to ensure
        that all words are lowercase, and that the word "pokemon" is written consistently.
        '''

        for pokemon in self.pokemon_dict:
            self.pokemon_dict[pokemon]['text'] = ['pokemon' if token.lower() ==  'pokémon' else token.lower() for token in self.pokemon_dict[pokemon]['text']]

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
        Returns the 25 Pokemon with the highest bm25 scores and their image file paths.
        This will be used to serve the results.
        '''

        preprocessed_query = self.query_preprocessing(query)

        # Create a vector to store the results for each Pokemon.
        results_vec = np.zeros(len(self.pokemon_dict))

        # Iterate through each Pokemon
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

            # Store the score for the Pokemon in the results_vec array.     
            results_vec[index] = bm25_score

        # Get the 25 Pokemon with the highest bm25 score in descending order
        most_similar_pokemon_index = np.argsort(results_vec,-1)[::-1][:25]


        # Getting the names of each Pokemon in another vector to indexing later.
        self.pokemon_names = [pokemon for pokemon in self.pokemon_dict]
        pokemon_names = list(np.array(self.pokemon_names)[most_similar_pokemon_index])

        return dict([(pokemon, self.pokemon_dict[pokemon]['image']) for pokemon in pokemon_names])

