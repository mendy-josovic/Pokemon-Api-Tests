import pytest
import requests
import json
TEST_URLS = {'typeurl': 'https://pokeapi.co/api/v2/type', 'firetype': 'https://pokeapi.co/api/v2/type/10'}
TOP_5_WEIGHTS = {'charizard-gmax': 10000, 'cinderace-gmax': 10000, 'coalossal-gmax': 10000, 'centiskorch-gmax': 10000, 'groudon-primal': 9997}


def test_verify_type_count(): # using requests and json packages to extract the response from the first API
    response = json.loads(requests.get(TEST_URLS['typeurl']).content)
    assert response.get('count') == len(response.get('results'))# validating the result count is equal to the count field


def test_validate_fire_pokemon():
    response = json.loads(requests.get(TEST_URLS['firetype']).content)
    pokemons = response.get('pokemon')
    pokemons_names =[entry['pokemon']['name'] for entry in pokemons]# getting all pokemon names
    assert 'charmander' in pokemons_names
    assert 'bulbasaur' not in pokemons_names

def test_validate_top_5():
    response = json.loads(requests.get(TEST_URLS['firetype']).content)
    pokemons = response.get('pokemon')
    pokemon_urls =[{'name': entry['pokemon']['name'], 'url': entry['pokemon']['url']} for entry in pokemons] # getting all pokemon names and urls ia dict
    names_and_weights ={}
    for url in pokemon_urls: # getting all weights of pokemons
        weight = get_weight(url['url'])
        names_and_weights.update({url['name']: weight})


    sorted_dict = dict(sorted(names_and_weights.items(), key=lambda x: x[1], reverse=True))# sorting descending the list by the weights
    top_5 = dict(list(sorted_dict.items())[:5]) # getting the first 5
    assert top_5 == TOP_5_WEIGHTS


def get_weight(url):
    response = json.loads(requests.get(url).content)
    return response.get('weight')
