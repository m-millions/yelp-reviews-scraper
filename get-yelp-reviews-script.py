# -*- coding: utf-8 -*-
"""
This program uses Yelp"s Fusion API to:
(1) Query for a specific business --->>> GET https://api.yelp.com/v3/businesses/search
    using the criteira: "categories", "location", "name" in the query string, and 
(2) Once the page url is extracted for a business, scrape the reivews and ratings for 
    that specific business
(3) Query for a set number of business reviews using the passed value in "reviews" 
"""
from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import string
import urllib

from lxml import html
from urllib import quote, urlencode
from urllib2 import HTTPError


# Before accessing the Fuse API end-point, you must creat an 
# app and credentials.  Please go to the following link, and when
# you have them plug them in below, before attempting to run 
# the code --->>> https://www.yelp.com/developers/v3/manage_app
#REMOVE FOR DESTRIBUTION
#CLIENT_ID = 'insert-creds-here'
#CLIENT_SECRET = 'insert-creds-here'
CLIENT_ID = 'provided your own'
CLIENT_SECRET = 'provided your own'

# API constants for YELP's API
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come AFTER slash.
REVIEWS_PATH = '/reviews'  # Business ID will come BEFORE slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'

# DEFAULT search categoriess if none are provided by the User.
DEFAULT_CATEGORIES = 'pizza'
DEFAULT_LOCATION = 'New York, NY'
DEFAULT_REVIEWS_SEARCH_LIMIT = 3
DEFAULT_NAME = "Juliana's Pizza"

BUSINESS_SEARCH_LIMIT = 0
REVIEWS_SEARCH_LIMIT = 0


#2 - Second funtion called - REMOVE this COMMENT AT WILL.
def get_bearer_token(host, path):
    """Given a bearer token, sends a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        str: OAuth bearer token -- using client_id and client_secret.
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

#4 - Fourth function called - REMOVE this COMMENT AT WILL.
def get_reviews(business_id, page, reviews_limit):
    """
    Query the Business API by a business ID.
    """
    page = requests.get(page)
    tree = html.fromstring(page.content)
    #This will create a list of reviews: 
    reviews = tree.xpath('//p[@itemprop="description"]/text()')
    ratings = tree.xpath(".//div[contains(@class,'rating-large')]//@title")

    review = {}
    all_reviews = [business_id]
    
    count = int(reviews_limit) #converts passed value to interger for proper processing
    new_count = 0
    for i in reviews:
        if new_count < count:
            print('new count: ', new_count) # DELETE AT WILL
            review['review'] = filter(lambda x: x in string.printable, i)
            review['rating'] = ratings[new_count]
            all_reviews.append(review)
            review = {}
            new_count += 1     
    return all_reviews

#CANDIDATE FOR DEPRICATION
def get_reviews_old(bearer_token, business_id):
    """
    #CANDIDATE FOR DEPRICATION because this uses the Yelp API end-point 
    --->>> GET https://api.yelp.com/v3/businesses/{id}/reviews to retriew 
    reviews for a specific busineess

    However as of 07/03/2017 that API endpoint only returns the top three (3)
    reviews and only a snipet of each ...  We need more information than that.

    Please reference def get_reviews(business_id, page, reviews_limit) for full
    implementation
    """
    all_reviews = []
    review = []
    url_params = {'locale': 'en_US'}
    reviews_path = BUSINESS_PATH + business_id + REVIEWS_PATH
    
    response = request(API_HOST, reviews_path, bearer_token, url_params)
    print(u'Reviews for business "{0}" found:'.format(business_id))
    reviews = response.get('reviews')
    for i in reviews:
        review = i['text']
        print(review)
        all_reviews.append(review)    
    return all_reviews

#3 - Third funtion called - REMOVE this COMMENT AT WILL.
def send_request(host, path, bearer_token, url_params=None):
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
    headers = {'Authorization': 'Bearer %s' % bearer_token}

    print(u'Querying {0} ...'.format(url))
    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()

#1 - First funtion called - REMOVE this COMMENT AT WILL.
def get_businesses(categories, location, name, reviews_limit):
    """
    (1) gets a user token
    (2) Sends a fully qualified request to the API for a business with specific criteria
    (3) Searches response JSON objec for a specific business by name
    (4) If name is found and the business has a review count > 0, retrieves a specified
        number of reviews but < 10 per requirements ( this can be changed ... )
    """
    business_id = ''
    business_rating = ''
    url_params = {'categories': categories.replace(' ', '+'),
                  'location': location.replace(' ', '+'),
                  'limit': BUSINESS_SEARCH_LIMIT #not currently being used - set to 0, no param passed in
    }

    #2 - gets token 
    bearer_token = get_bearer_token(API_HOST, TOKEN_PATH)

    #3 - sends fully qualified request
    response = send_request(API_HOST, SEARCH_PATH, bearer_token, url_params)
    businesses = response.get('businesses')
    
    #print lenght businesses object -- REMOVE AT WILL
    pprint.pprint(len(businesses), indent=2)
    print('---------')
    name_found = 0
    for i in businesses:
        if i['name'] == name:
            name_found = 1
            business_id = i['id']
            business_name = i['name']
            business_rating = i['rating']
            review_count = i['review_count']
            page = i['url']
            print(u'ID: {0} NAME: {1} RATING: {2} REVIEW COUNT: {3} PAGE: {4}'.format(business_id, \
                    business_name, business_rating, review_count, page))
            break
   
    if name_found == 0:
        print(u'No businesses for {0} in {1} with the name {2} found.'.format(categories, location, name))
        return      
    
    print('---------')
    print(u'Match found, querying for ratings for: "{0}" in {1}...'.format(business_name, location))
    print('---------')

    #4 - If business has reviews, get reviews using retrieved business_id
    if review_count > 0:
        if review_count < int(reviews_limit): #only retriew the number of reviews specifed by criteria
            print('---------')
            print(u'actual review count: {0} vs. reviews limit you provided: {1}'.format(review_count, reviews_limit))
            print('---------')
            print(u'Less reviews than you requested were found for {0}'.format(name))
        #4 get reviews for the business    
        all_reviews = get_reviews(business_id, page, reviews_limit)
        return all_reviews
    else:
        print(u'No Reviews are available for {0}.'.format(name))
    return

#0 Logic starting point - REMOVE this COMMENT AT WILL.
def main():
    """
    (1) Makes a call to "get_business" passing the user defined args.
    (2) Arguments are:
        --- categories (str): Defines the category to search for ( e.g. "pizza")
        --- location (str): Limits the query to a geographic location (e.g. "New York, NY")
        --- name (str): Limits the query to spacific locale, by name
        --- reviews (str): Limits the number of reviews to be returned as < 10
    (3) If no arguments are provided, default values will kick in
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--categories', dest='categories', default=DEFAULT_CATEGORIES,
                        type=str, help='Search categories (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')
    parser.add_argument('-n', '--name', dest='name',
                        default=DEFAULT_NAME, type=str,
                        help='Search name (default: %(default)s)')
    parser.add_argument('-r', '--reviews', dest='reviews',
                        default=DEFAULT_REVIEWS_SEARCH_LIMIT, type=str,
                        help='Search name (default: %(default)s)')
    input_values = parser.parse_args()

    try:
        print('---------') #persist to console values passed in at command line - REMOVE AT WILL.  
        print(input_values.categories, input_values.location, input_values.name,input_values.reviews)
        print('---------')
        #1 Look up if a business exists with the passed criteria
        all_reviews = get_businesses(input_values.categories, input_values.location, input_values.name,input_values.reviews)
        print('---------')     
        pprint.pprint(all_reviews)
        print('---------')

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

