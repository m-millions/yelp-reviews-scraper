Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.

There are two scripts in this repository:

(1) "get-yelp-business-by-category-location.py"

Returns a specified number of yelp reviews for a category/location

This program requires the Python requests library, which you can install via:
`pip install -r requirements.txt`.

Sample usage of the program:
`python get-yelp-reviews.py --categories="pizza" --location="New York, NY" 

SAMPLE/ACTUAL YELP BUSINESS for PIZZA and NEW YORK, NY
    Juliana's Pizza, Prince Street Pizza, Lombardi's , L'industrie Pizzeria
    Patzeria Perfect Pizza, My Pie, Joe's Pizza, NY Pizza Suprema
    B Side Pizza & Wine Bar, Adrienne's Pizzabar, La Margarita Pizza
    Rubirosa, Stage Door Pizza, Patsys Pizzeria, Paulie Gee's
    Sottocasa Pizzeria- Boerum Hill, Barboncino Pizza & Bar, Joe's Pizza
    PN Wood Fired Pizza, B Squared

SAMPLE/ACTUAL JSON object retured:
Juliana's Pizza julianas-pizza-brooklyn-5 {u'city': u'Brooklyn', u'display_address': 
                                           [u'19 Old Fulton St', u'Brooklyn, NY 11201'], 
                                            u'country': u'US', u'address2': u'', 
                                            u'address3': u'', u'state': u'NY', 
                                            u'address1': u'19 Old Fulton St', u'zip_code': u’11201'}
Prince Street Pizza prince-street-pizza-new-york-2 {u'city': u'New York', u'display_address': 
                                                    [u'27 Prince St', u'New York, NY 10012'], 
                                                     u'country': u'US', u'address2': u'', 
                                                     u'address3': u'', u'state': u'NY', 
                                                     u'address1': u'27 Prince St', u'zip_code': u’10012'}

(2) "get-yelp-reviews-script.py"

