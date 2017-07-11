# -*- coding: utf-8 -*-
"""
This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search categories, location, name
and the Business API to query additional information about the top result
from the search query.

Sample usage of the program:
`python get-yelp-reviews.py --categories="pizza" --location="New York, NY" 

SAMPLE/ACTUAL YELP BUSINESS for PIZZA and NEW YORK, NY
    Juliana's Pizza, Prince Street Pizza, Lombardi's , L'industrie Pizzeria
    Patzeria Perfect Pizza, My Pie, Joe's Pizza, NY Pizza Suprema
    B Side Pizza & Wine Bar, Adrienne's Pizzabar, La Margarita Pizza
    Rubirosa, Stage Door Pizza, Patsys Pizzeria, Paulie Gee's
    Sottocasa Pizzeria- Boerum Hill, Barboncino Pizza & Bar, Joe's Pizza
    PN Wood Fired Pizza, B Squared
"""
from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib

from urllib import quote, urlencode
from urllib2 import HTTPError


# OAuth credential placeholders that must be filled in by users.
# You can find them on
# https://www.yelp.com/developers/v3/manage_app
CLIENT_ID = 'provided your own'
CLIENT_SECRET = 'provided your own'

# API constants for YELP's API
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'

# DEFAULT search categoriess if none are provided by the User.
DEFAULT_CATEGORIES = 'pizza'
DEFAULT_LOCATION = 'New York, NY'

#SAMPLE NAMES TO USE FOR TESTING
DEFAULT_NAME = 'paulie-gees-brooklyn'
SEARCH_LIMIT = 0

#4
def request(host, path, bearer_token, url_params=None):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

#3
def get_business(bearer_token, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    #4
    return request(API_HOST, business_path, bearer_token)

#2
def obtain_bearer_token(host, path):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        str: OAuth bearer token, obtained using client_id and client_secret.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    assert CLIENT_ID, "Please supply your client_id."
    assert CLIENT_SECRET, "Please supply your client_secret."
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token

#1
#def query_api(categories, location):
def query_api(categories, location):
    """Queries the API by the input values from the user.
    
    Args:
        categories (str): The search categories to query.
        location (str): The location of the business to query.
        name (str): The name of the business to query.
    """
    url_params = {
        'categories': categories.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }

    #2
    bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)

    #3
    response = request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)
    businesses = response.get('businesses')
    #print lenght businesses object -- REMOVE AT WILL
    pprint.pprint(len(businesses), indent=2)
    
    business = ''
    business_id = ''
    business_location = ''
    print('---------')    
    for i in businesses:
        business = i['name']
        business_id = i['id']
        business_location = i['location']
        print(business, business_id, business_location)
    print('---------')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(categories, location, name))
        return
    

#0
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--categories', dest='categories', default=DEFAULT_CATEGORIES,
                        type=str, help='Search categories (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')
    
    input_values = parser.parse_args()

    try:
        #1
        query_api(input_values.categories, input_values.location)
        #query_api(input_values.categories, input_values.location, input_values.name)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()

