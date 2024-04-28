# Flask stuff
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for
import requests



from pokemon_search import PokemonSearch
import pickle


app = Flask(__name__, static_url_path='', static_folder='staticpages', template_folder='staticpages')

with open('pokemon.pickle', 'rb') as f:
    pokemon_dict = pickle.load(f)

pokemon_search = PokemonSearch().create_index(pokemon_dict)

# Home page for unauthorized users
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def run_user_query():

    if not request.json:
        abort(400)

    query = request.json

    query_results = pokemon_search.query(query)

    results = []

    for pokemon, image in query_results.items():
        poke_dict = {}
        poke_dict['name'] = pokemon
        poke_dict['image'] = image
        results.append(poke_dict)

    return jsonify(results)


#if __name__ == '__main__':
 #   with open('pokemon.pickle', 'rb') as f:
  #      pokemon_dict = pickle.load(f)
    
   # pokemon_search = PokemonSearch().create_index(pokemon_dict)

    #user_query = input("Please enter your query: \n")
    #print("Your results are:")
    #print(pokemon_search.query(user_query))

