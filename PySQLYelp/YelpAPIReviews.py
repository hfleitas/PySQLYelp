from yelpapi import YelpAPI
from pprint import pprint

# yelpapi requires api key to join Developer Beta.
## ref: https://www.yelp.com/developers/v3/manage_app

app_secret = 'app_secret' #api key
yelp_api = YelpAPI(app_secret)

"""
    Example reviews query.
    
    Reviews API: https://www.yelp.com/developers/documentation/v3/business_reviews
"""
print("***** selected reviews for Universal Property and Casualty Insurance Company in Fort Lauderdale. *****\n{}\n".format("yelp_api.reviews_query(id='universal-property-and-casualty-insurance-company-fort-lauderdale')"))
try:
    response = yelp_api.reviews_query(id='universal-property-and-casualty-insurance-company-fort-lauderdale')
    pprint(response)
except YelpAPI.YelpAPIError as e:
    print(e)
print('\n-------------------------------------------------------------------------\n')
