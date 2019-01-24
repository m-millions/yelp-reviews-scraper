
There are two scripts in this repository, and they both use Yelp's Fusion API
to return a JSON object.

Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.

SAMPLE/ACTUAL YELP BUSINESS for PIZZA and NEW YORK, NY ( pick one ):
```
    Juliana's Pizza, Prince Street Pizza, Lombardi's , L'industrie Pizzeria
    Patzeria Perfect Pizza, My Pie, Joe's Pizza, NY Pizza Suprema
    B Side Pizza & Wine Bar, Adrienne's Pizzabar, La Margarita Pizza
    Rubirosa, Stage Door Pizza, Patsys Pizzeria, Paulie Gee's
    Sottocasa Pizzeria- Boerum Hill, Barboncino Pizza & Bar, Joe's Pizza
    PN Wood Fired Pizza, B Squared
```

(1) "get-yelp-business-by-category-location.py"

Returns a specified number of yelp reviews for a category/location

This program requires the Python "requests" and "lxml" libraries, which you can install via:
'pip install -r requirements.txt'.

Sample usage of the program:
`python get-yelp-reviews.py --categories="pizza" --location="New York, NY"` 

SAMPLE/ACTUAL JSON object retured:
```
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
```

(2) "get-yelp-reviews-script.py"

This program uses Yelp"s Fusion API to:
(1) Query for a specific business --->>> GET https://api.yelp.com/v3/businesses/search
    using the criteira: "categories", "location", "name" in the query string 
(2) Once the page url is extracted for a business, scrape the reivews and ratings for 
    that specific business
(3) Query for a set number of business reviews using the passed value in "reviews" 

Sample usage of the program, but running at the command line --->>>
`python get-yelp-reviews-v7.py --categories="pizza" --location="New York, NY" --name="Patsys Pizzeria" --reviews="5"`

Alternatively, run without input ( hard-coded default values will take over... )

SAMPLE/ACTUAL JSON object retured:
```
{
  "name": "Juliana's Pizza",
  "reviews": [
    {
      "rating": "5.0 star rating",
      "review": "Let me start off by saying I've tried all the best pizza joints in the city. Lombardi's, Paulie Gee's, you name it. I've even had Grimaldi's in Scottsdale, AZ and in California. They're all great in their own ways, but to me Juliana's hits the spot every single time. This is the quintessential NY pie.\n\nAgain, to me this is the best pizza in NYC, and maybe the world. Crust and dough are perfect. Little bit of coal fired char on the outer rim, and nice and doughy on the inside. Mozzarella cheese is chewy and tasty. Ricotta is smooth and flavorful. The sauce is made from tomatoes important from Italy and vibrant and flavorful, but also not overbearing. We went with a white and a half sausage onion/half pepperoni. The owner is also awesome. Super friendly guy and is passionate about pizza!"
    },
    {
      "rating": "4.0 star rating",
      "review": "Brooklyn Pizza!! \nWow!! Looooong lines for Juliana's Pizza in the raining evening.... We gave up waiting line and takeout Pizza instead!! Since we stayed really close @1 Hotel Brooklyn!! \nWe takeout Salad and Half Margarita and White pizza with prosciutto!! \nPizza was pretty good but I wouldn't want to wait over hour for this pizza. I know better pizza places in Japan!!"
    },
    {
      "rating": "5.0 star rating",
      "review": "If you want the AUTHENTIC Grimaldi's pizza, this is the place to go. Grimadi's is actually not operated my Grimaldi, he sold the franchise and opened Juliana's in the name of his mother. I remember coming here a few years back and the pizza was delicious. Good pizza like this is one of the few times where I do not mind devouring/ vacuuming in carbs into my stomach. I was blessed with the opportunity to meet Grimaldi himself. It was a winter day and not much people were in the restaurant. An elder man came over and asked how were were doing and such. My sister and I's face lit up like we had the matching numbers to a billion dollar powerball when he introduced himself. I noticed that he was eating something and I asked \"What it was?\" and he said it was eggplant parm. I said \"Oh I don't usually like eggplant (my mom butchers eggplant, steams it and puts oyters sauce like your typical asian) and it doesn't taste good to me.\" In the midst of our excitement, I asked if we could take a picture and he was really kind and gentle and agreed to it. After he left the table, and a few moments later, the waiter brings out a plate with some sort of fried looking thing to me. I took one to eat and I was like wow this is really good to my sister \"What is it?\" She said \"It's eggplant parm.\" I see what you did there Mr. Grimaldi :) Thank you.\n\nIf you are ever around NYC, I'd 100% recommend his place. It's near the Dumbo area, which is a nice place to walk around for a date or family stop by this gem. \n\nI know this picture isn't the best quality or most up to date, but this was an experience I'd never forget.\n\nThis plaice does get crowed fast!"
    },
    {
      "rating": "5.0 star rating",
      "review": "Given there is no shortage of quality pizzerias in NYC it may seem absurd to wait in line for one - but honestly, Juliana's is well worth it. \n\nWe went around 4pm on a Saturday and the line was beyond the cordons they have set up. In the end we waited about 45 mins, which is not that bad (when you compare to say waiting 2hrs for a milkshake at Black Tap or the Dumbo ride at Disney...). It's well organised and they check the party sizes in the line so that they can arrange the tables accordingly. \n\nOnce seated it's relatively cosy but not to the point where other tables are interfering with your enjoyment. The walls (or at least the one I was looking at) are covered in pictures of Sinatra. \n\nYou have a choice of classic pizzas that you can add extra toppings or their specialties, to which you can make no changes. We went for a Margherita with pepperoni (wife's pick) plus the No. 1 special (a white pizza with mozzarella, scamorza affumicata and pancetta). Both were great but the special was the stand out dish - so good - best pizza I've had. Didn't have specs for one of their \"sweets\" as we had two larges and I was stuffed - but I had the Brookie bridge (ice cream sandwich with brownies) a couple of years ago and if i remember correctly it was great. \n\nGotta shout out to our waiter Trimell - not just for being a great waiter, but also while we were waiting in line he ran after a customer that had left their card behind"
    },
    {
      "rating": "4.0 star rating",
      "review": "What's not to like about great ambience, really good margarita pizza, pasta puttanesca al dente, and an amazing Caesar salad with white anchovies?"
    }
  ],
  "uri": "http://localhost:5000/get-reviews/api/v1.0/reviews/pizza/New%20York%2C%20NY/Juliana%27s%20Pizza/5"
}
```

