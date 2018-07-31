# We import the requests module which allows us to make the API call
import requests
 
# Replace [app_id] with the App ID and [app_secret] with the App Secret
app_id = 'app_id'
app_secret = 'app_secret'
data = {'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret}
#token = requests.post('https://api.yelp.com/oauth2/token', data = data)
#access_token = token.json()['access_token']
headers = {'Authorization': 'Bearer %s' % app_secret}
 
# Call Yelp API to pull business data for UPCIC 
biz_id = 'universal-property-and-casualty-insurance-company-fort-lauderdale'
url = 'https://api.yelp.com/v3/businesses/{}/reviews'.format(biz_id)
response = requests.get(url = url, headers = headers)
response_data = response.json()

print(response_data)

