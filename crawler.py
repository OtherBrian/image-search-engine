from PIL import Image
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import pickle  
nltk.download('stopwords') 


def get_pokemon():
    '''
    Crawls the main index of Bulbapedia to get the names of each Pokemon.
    Returns a dictionary with the names of each Pokemon as the key.
    Each Pokemon has a subdictionary for which URL is currently their only key.
    '''

    pokemon_dict = {}

    base_url = 'https://bulbapedia.bulbagarden.net'
    response = requests.get(f"{base_url}/wiki/List_of_Pok%C3%A9mon_by_name")
    soup = BeautifulSoup(response.text, 'html.parser')

    # Inspecting the html shows that I only want the roundy tables on the page.
    tables = soup.find_all('table', class_='roundy')
    for table in tables:
        links = table.find_all('a')
        for link in links:
            if link.find('img'):
                pokemon_name = link['title']
                pokemon_link = link['href']
            
                pokemon_dict[pokemon_name] = {}
                pokemon_dict[pokemon_name]['url'] = pokemon_link

    return pokemon_dict


### Pre-processing ###

def token_stem_stopwords(text, tokenizer):

    '''
    Tokenizes the given text and removes any stopwords.
    Returns the tokens as a list.
    '''

    text_tokens = tokenizer.tokenize(text)
    text_tokens_without_sw = [word.lower() for word in text_tokens if not word in stopwords.words()]

    return text_tokens_without_sw


def crawl_pokemon(pokemon_dict):
    '''
    Iterates through each Pokemon in the dictionary.
    Concantentates, then pre-processes the text on the page.
    Downloads and saves the primary image of the page.
    Returns an updated pokemon_dict with the tokenized text and image url for each Pokemon.
    '''

    # The following Pokemon have multiple forms, and so their images have different names.
    unusual_pokemon = {
        'Deerling': 'Spring Form',
        'Enamorus': 'Incarnate Forme',
        'Flabébé': 'Red Flower',
        'Floette': 'Red Flower',
        'Florges': 'Red Flower',
        'Gimmighoul': 'Chest Form',
        'Hippopotas': 'Male',
        'Hippowdon': 'Male',
        'Keldeo': 'Ordinary Form',
        'Landorus': 'Incarnate Forme',
        'Lycanroc': 'Midday Form',
        'Morpeko': 'Full Belly Mode',
        'Maushold': 'Family of Four',
        'Meloetta': 'Aria Forme',
        'Mimikyu': 'Disguised Form',
        'Minior': 'Meteor Form',
        'Ogerpon': 'Teal Mask',
        'Oricorio': 'Baile Style',
        'Palafin': 'Zero Form',
        'Sawsbuck': 'Spring Form',
        'Shaymin': 'Land Forme',
        'Squawkabilly': 'Green Plumage',
        'Tatsugiri' : 'Curly Form',
        'Terapagos': 'Normal Form',
        'Thundurus': 'Incarnate Forme',
        'Tornadus': 'Incarnate Forme',
        'Toxtricity': 'Amped Form',
        'Urshifu': 'Single Strike Style',
        'Wishiwashi': 'Solo Form',
        'Wormadam': 'Plant Cloak',
        'Xerneas': 'Active Mode',
        'Zacian': 'Hero of Many Battles',
        'Zamazenta': 'Hero of Many Battles',
        'Zygarde': '50% Forme'
    }

    # Instantiating the tokenizer to be used for pre-processing.
    tokenizer = RegexpTokenizer(r'\w+')

    ## This process can take hours, so using a simple method to ensure anything that has previously been stored doesn't get re-done.
    completed_pokemon = set()
    for pokemon in pokemon_dict:
        if 'image' in pokemon_dict[pokemon]:
            completed_pokemon.add(pokemon)

    # Adding a counter to track progress, since this can take hours to run.
    counter = 1
    length = len(pokemon_dict)
    remaining_length = length - len(completed_pokemon)

    for pokemon in pokemon_dict:
        if pokemon not in completed_pokemon:
            pokemon_url = f"{base_url}{pokemon_dict[pokemon]['url']}"
        
            response = requests.get(pokemon_url)
            soup = BeautifulSoup(response.text, 'html.parser')
        
            # These tags ensure I'm not getting advertisements and such.
            pokemon_facts = soup.find_all(['p', 'h1', 'h2', 'h3']) +  soup.find_all('table', class_='roundy')
            # Combine the text output into one large string to be tokenized
            pokemon_string = ''
            for fact in pokemon_facts:
                pokemon_string += f" {str(fact.text)}"
        
            pokemon_string_tokenized = token_stem_stopwords(pokemon_string, tokenizer)
            pokemon_dict[pokemon]['text'] = pokemon_string_tokenized
        
            if pokemon in unusual_pokemon:
                pokemon_image_ref = soup.find('a', title=f"{unusual_pokemon[pokemon]}")
            else:
                pokemon_image_ref = soup.find('a', title=f"{pokemon}")
                
            pokemon_image_url = pokemon_image_ref.find('img')['src']
            pokemon_image_filepath = f"images/{pokemon}.png"
        
            image = Image.open(requests.get(f"https:{pokemon_image_url}", stream = True).raw)
            image.save(pokemon_image_filepath)
            
            pokemon_dict[pokemon]['image'] = pokemon_image_filepath
        
            print(f"{pokemon} done. {counter}/{remaining_length} complete.")
            
            counter += 1
        
    return pokemon_dict


if __name__ == '__main__':
    pokemon_dict = get_pokemon()
    completed_pokemon_dict = crawl_pokemon(pokemon_dict)

    # Storing the dictionary to be used in the next script.
    pickle.dump(pokemon_dict, open("pokemon.pickle", "wb"))