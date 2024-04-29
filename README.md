# Image Search Engine assignment 2024

This repository includes a simple example utilizing BM25 for image retrieval. I've used a Pokémon search engine as my example by crawling the images and text content for each Pokémon found on [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Main_Page). 

While this assignment is being assessed, an example of the retrieval app in action can be found at https://mcnubn.pythonanywhere.com/ 

## Repository Contents

**app.py:** This is a Flask app which loads pokemon.pickle, and instantiates a PokemonSearch object. It also renders a simple html page, and formats query results so that they can be easily displayed on the webpage via JavaScript.

**crawler.py** This script crawls each of the Pokémon found on [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/). As part of the crawling process, the main image for each Pokémon is stored in the images2 folder. The text on each Pokémon's dedicated page is also stored and tokenized. This is saved to pokemon.pickle. 

**pokemon_search.py** This script creates the PokemonSearch class to be used for querying in app.py. The tokenized text for each Pokémon (stored in pokemon.pickle) is used to create an inverted index, which is then used alongside a simple BM25 implementation when a query is provided. 

**pokemon.pickle** The pickle file containing the output of crawler.py.

**images2 folder** This folder contains an image for each Pokémon, as retrieved via crawler.py

**staticpages folder** This folder contains a simple HTML webpage, CSS file and JavaScript file. These provide a basic front end for the Flask app which is being hosted on PythonAnywhere.

**requirements.txt:** The Python libraries required to run the Python scripts in this repository. This can be used to set up a virtual environment to run the script in. You can find more details on this below.

**README.md:** You are currently reading this file. It provides an overview of this repository and its contents.


## How to use this repository

### Installing Python and required libraries

In order to run the searchengine.py script in this repository, you will require Python to be installed on the machine. This was created with Python version 3.11.7.

You can install Python via [Python.org](https://www.python.org/downloads/).

As for the libraries that are required, in order to run the app itself you will need:
* numpy
* nltk
* Flask

If you wish to run crawler.py too you will also need:
* beautifulsoup4
* Pillow
* Requests

You can install these individually via the command line by typing ([as outlined here](https://datatofish.com/install-package-python-using-pip/)):

```pip install [package name]```

Alternatively you can install all of these packages via the requirements.txt file by typing the following into the command line:

```pip install -r requirements.txt```


### Cloning the repository and running it on a local machine

You can find up to date steps on how to clone a Github repository [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).
